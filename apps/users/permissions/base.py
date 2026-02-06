from rest_framework.permissions import BasePermission
from apps.users.enums.role import RoleEnum


class IsOwner(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.role.code == RoleEnum.OWNER


class IsOwnerOrAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.role.code in [RoleEnum.OWNER, RoleEnum.ADMINISTRATOR]


class IsStaffMember(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff