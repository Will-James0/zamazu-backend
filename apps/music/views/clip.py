from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.music.models import Clip
from apps.music.serializers.clip import ClipSerializer, CreateClipSerializer, UpdateClipSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import base as user_perms


class ClipListView(generics.ListAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class ClipDetailView(generics.RetrieveAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class ClipCreateView(generics.CreateAPIView):
    queryset = Clip.objects.all()
    serializer_class = CreateClipSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Clip créé avec succès."}, status=status.HTTP_201_CREATED)
    
    
class ClipUpdateView(generics.UpdateAPIView):
    queryset = Clip.objects.all()
    serializer_class = UpdateClipSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Clip mis à jour avec succès."}, status=status.HTTP_200_OK)
    
    
class ClipDeleteView(generics.DestroyAPIView):
    queryset = Clip.objects.all()
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def delete(self, request, *args, **kwargs):
        clip = self.get_object()
        clip.video_file.delete(save=False)
        clip.delete()
        return Response({"message": "Clip supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)