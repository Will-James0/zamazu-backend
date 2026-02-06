from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.music.models import Album
from apps.music.serializers.album import AlbumSerializer, CreateAlbumSerializer, UpdateAlbumSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import base as user_perms


class AlbumListView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class AlbumDetailView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

class AlbumCreateView(generics.CreateAPIView):
    queryset = Album.objects.all()
    serializer_class = CreateAlbumSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Album créé avec succès."}, status=status.HTTP_201_CREATED)
    

class AlbumUpdateView(generics.UpdateAPIView):
    queryset = Album.objects.all()
    serializer_class = UpdateAlbumSerializer
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Album mis à jour avec succès."}, status=status.HTTP_200_OK)
    

class AlbumDeleteView(generics.DestroyAPIView):
    queryset = Album.objects.all()
    lookup_field = 'code'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, user_perms.IsOwnerOrAdmin]
    
    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        album.cover_image.delete(save=False)
        album.delete()
        return Response({"message": "Album supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    