from rest_framework.permissions import BasePermission

class IsProfileOwner(BasePermission):
    """
    Permission to check if the user is the owner of the profile.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user