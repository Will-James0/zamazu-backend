# apps/users/serializers/user.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import Role
from apps.users.enums import RoleEnum

User = get_user_model()

class PublicRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['code', 'name']
        read_only_fields = ['code', 'name']

class UserSerializer(serializers.ModelSerializer):
    role = PublicRoleSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'role', 'phone', 'code', 'image'
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']
        

class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_null=True)
    last_name = serializers.CharField(allow_null=True)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    
    def validate_role(self, value):
        if not Role.objects.filter(code=value).exists():
            raise serializers.ValidationError("Rôle invalide.")
        
        # Vérifier les permissions de l'utilisateur qui crée
        request = self.context.get('request')
        if request and request.user:
            current_user_role = request.user.role.code
            
            # Hiérarchie des rôles (du plus élevé au plus bas)
            role_hierarchy = {
                RoleEnum.OWNER: 4,
                RoleEnum.ADMINISTRATOR: 3,
                RoleEnum.MODERATOR: 2,
                RoleEnum.MEMBER: 1,
            }
            
            current_level = role_hierarchy.get(current_user_role, 0)
            target_level = role_hierarchy.get(value, 0)
            
            # Le owner peut tout faire
            if current_user_role == RoleEnum.OWNER:
                return value
            
            # L'admin ne peut pas créer d'admin ou de owner
            if current_user_role == RoleEnum.ADMINISTRATOR:
                if value in [RoleEnum.OWNER, RoleEnum.ADMINISTRATOR]:
                    raise serializers.ValidationError(
                        "Vous n'avez pas la permission de créer un utilisateur avec ce rôle."
                    )
            
            # Le modérateur ne peut créer que des membres
            if current_user_role == RoleEnum.MODERATOR:
                if value != RoleEnum.MEMBER:
                    raise serializers.ValidationError(
                        "Vous ne pouvez créer que des utilisateurs avec le rôle 'member'."
                    )
            
            # Les membres ne peuvent rien créer
            if current_user_role == RoleEnum.MEMBER:
                raise serializers.ValidationError(
                    "Vous n'avez pas la permission de créer des utilisateurs."
                )
        
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Nom d'utilisateur déjà pris.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email déjà utilisé.")
        return value
    
    def create(self, validated_data):
        role = Role.objects.get(code=validated_data.pop('role'))
        user = User.objects.create_user(
            role=role,
            **validated_data
        )
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password', 'role'
        ]
        extra_kwargs = {
            'password': {'allow_blank': True, 'write_only': True, 'required': False},
            'email': {'required': False},
            'username': {'required': False},
            'first_name': {'allow_null': True},
            'last_name': {'allow_null': True},
        }
    
    def validate_role(self, value):
        if not Role.objects.filter(code=value).exists():
            raise serializers.ValidationError("Rôle invalide.")
        
        # Vérifier les permissions pour modifier le rôle
        request = self.context.get('request')
        if request and request.user and self.instance:
            current_user_role = request.user.role.code
            target_user_current_role = self.instance.role.code
            new_role = value
            
            # Hiérarchie des rôles
            role_hierarchy = {
                RoleEnum.OWNER: 4,
                RoleEnum.ADMINISTRATOR: 3,
                RoleEnum.MODERATOR: 2,
                RoleEnum.MEMBER: 1,
            }
            
            current_level = role_hierarchy.get(current_user_role, 0)
            target_current_level = role_hierarchy.get(target_user_current_role, 0)
            new_level = role_hierarchy.get(new_role, 0)
            
            # Le owner peut tout modifier
            if current_user_role == RoleEnum.OWNER:
                # Mais ne peut pas se rétrograder lui-même (protection)
                if self.instance.id == request.user.id and new_role != RoleEnum.OWNER:
                    raise serializers.ValidationError(
                        "Le propriétaire ne peut pas se rétrograder lui-même."
                    )
                return value
            
            # L'admin ne peut pas toucher aux admins ni aux owners
            if current_user_role == RoleEnum.ADMINISTRATOR:
                if target_user_current_role in [RoleEnum.OWNER, RoleEnum.ADMINISTRATOR]:
                    raise serializers.ValidationError(
                        "Vous ne pouvez pas modifier le rôle de cet utilisateur."
                    )
                if new_role in [RoleEnum.OWNER, RoleEnum.ADMINISTRATOR]:
                    raise serializers.ValidationError(
                        "Vous ne pouvez pas promouvoir un utilisateur à ce niveau."
                    )
            
            # Le modérateur ne peut modifier que des membres
            if current_user_role == RoleEnum.MODERATOR:
                if target_user_current_role != RoleEnum.MEMBER:
                    raise serializers.ValidationError(
                        "Vous ne pouvez modifier que les membres."
                    )
                if new_role != RoleEnum.MEMBER:
                    raise serializers.ValidationError(
                        "Vous ne pouvez pas promouvoir les utilisateurs."
                    )
            
            # Les membres ne peuvent rien modifier (sauf eux-mêmes via IsOwnerOrAdmin)
            if current_user_role == RoleEnum.MEMBER:
                raise serializers.ValidationError(
                    "Vous n'avez pas la permission de modifier les rôles."
                )
        
        return value
    
    def validate_username(self, value):
        user = self.instance
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Nom d'utilisateur déjà pris.")
        return value
    
    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Email déjà utilisé.")
        return value
    
    def update(self, instance, validated_data):
        role_code = validated_data.pop('role', None)
        if role_code:
            role = Role.objects.get(code=role_code)
            instance.role = role
        
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    
class StatutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']