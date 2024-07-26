from rest_framework.permissions import BasePermission
from .models import User

class IsAuthenticatedUser(BasePermission):
    """Checks if user is authenticated."""
    def has_permission(self, request, view):
        """Checks if user is authenticated with the same token."""
        return str(request.user.id) == request.data.get('id') # checks if the user id is the same as the id in the request data.

    def has_object_permission(self, request, view, obj):
        return request.user == obj
