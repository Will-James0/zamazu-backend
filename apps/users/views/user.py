from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer, StatutUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsOwner, IsOwnerOrAdmin, IsStaffMember
from apps.users.enums import RoleEnum


User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffMember]
    
    
class UserCreateView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'code'
    
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'code'
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.image:
            instance.image.delete(save=False)
        
        # Empêcher l'auto-suppression
        if instance.id == request.user.id:
            return Response(
                {"detail": "Vous ne pouvez pas supprimer votre propre compte."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier la hiérarchie des rôles
        current_user_role = request.user.role.code
        target_user_role = instance.role.code
        
        role_hierarchy = {
            RoleEnum.OWNER: 4,
            RoleEnum.ADMINISTRATOR: 3,
            RoleEnum.MODERATOR: 2,
            RoleEnum.MEMBER: 1,
        }
        
        current_level = role_hierarchy.get(current_user_role, 0)
        target_level = role_hierarchy.get(target_user_role, 0)
        
        # Seul le owner peut tout faire
        if current_user_role != RoleEnum.OWNER:
            # Les admins ne peuvent pas supprimer d'autres admins ou owners
            if target_level >= current_level:
                return Response(
                    {"detail": "Vous ne pouvez pas supprimer cet utilisateur."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        return super().delete(request, *args, **kwargs)
    
class StatusToggleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def patch(self, request, code):  # PATCH au lieu de POST
        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        # Empêcher l'auto-désactivation
        if user.id == request.user.id:
            return Response(
                {"detail": "Vous ne pouvez pas modifier votre propre statut."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier la hiérarchie des rôles
        current_user_role = request.user.role.code
        target_user_role = user.role.code
        
        role_hierarchy = {
            RoleEnum.OWNER: 4,
            RoleEnum.ADMINISTRATOR: 3,
            RoleEnum.MODERATOR: 2,
            RoleEnum.MEMBER: 1,
        }
        
        current_level = role_hierarchy.get(current_user_role, 0)
        target_level = role_hierarchy.get(target_user_role, 0)
        
        # Seul le owner peut tout faire
        if current_user_role != RoleEnum.OWNER:
            # Les admins ne peuvent pas désactiver d'autres admins ou owners
            if target_level >= current_level:
                return Response(
                    {"detail": "Vous ne pouvez pas modifier le statut de cet utilisateur."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        user.is_active = not user.is_active
        user.save()
        
        serializer = StatutUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)