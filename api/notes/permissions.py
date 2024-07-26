from rest_framework.permissions import BasePermission
from .models import Note

class IsNotesOwner(BasePermission):
    """Checks if user is authenticated."""
    def has_permission(self, request, view):
        """Checks token authentication user is the same Notes owner"""
        return request.user.username == view.kwargs['username'] 

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsTheNoteOwner(BasePermission):
    """Checks if user is authenticated."""
    def has_permission(self, request, view):
        """Checks token authentication user is the same Note owner"""
        note = Note.objects.get(id=view.kwargs['note_id'])
        return request.user == note.user

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user