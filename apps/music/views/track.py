from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.music.models import Album, Track
from apps.music.serializers.track import TrackSerializer, CreateTrackSerializer, UpdateTrackSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import base as user_perms


class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class TrackDetailView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class TrackCreateView(generics.CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = CreateTrackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Track créé avec succès."}, status=status.HTTP_201_CREATED)
    
    
class TrackUpdateView(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = UpdateTrackSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Track mis à jour avec succès."}, status=status.HTTP_200_OK)
    
    
class TrackDeleteView(generics.DestroyAPIView):
    queryset = Track.objects.all()
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def delete(self, request, *args, **kwargs):
        track = self.get_object()
        track.cover_image.delete(save=False)
        track.audio_file.delete(save=False)
        track.delete()
        return Response({"message": "Track supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)