from rest_framework.permissions import BasePermission
from .models import Profile

class IsProfileOwner(BasePermission):
    """Checks if user is authenticated."""
    def has_permission(self, request, view):
        """Checks token authentication user is the same profile owner"""
        return request.user.username == view.kwargs['username'] 

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
