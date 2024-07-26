from .models import Note
from .serializers import NoteSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsNotesOwner, IsTheNoteOwner
from .utils import assign_shared_with

class NotesBaseView(APIView):
    """View users profile based on username suffix."""
    permission_classes = [IsNotesOwner]
    def get_object(self, username):
        notes = Note.objects.filter(user__username=username)
        return notes

    def get(self, request, username):
        notes = self.get_object(username)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        request.data['user'] = request.user.id
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class NoteModifyView(APIView):
    """Edit profile view"""
    permission_classes = [IsTheNoteOwner]

    def get_object(self, note_id):
        note = Note.objects.get(id=note_id)
        return note

    def get(self, request, note_id):
        note = self.get_object(note_id)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, note_id):
        note = self.get_object(note_id)
        
        if request.data.get('shared_with'): # if shared_with is provided
            assign_shared_with(users=request.data.pop('shared_with'), note = note) # assign shared_with users to the note.
        
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = self.get_object(note_id)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedNotesView(APIView):
    """View shared notes."""
    permission_classes = [AllowAny]

    def get(self, request, share_id):
        note = Note.objects.get(share_id=share_id)
        serializer = NoteSerializer(note)
        
        if note.is_public_shared: # if the note is public.
            return Response(serializer.data)
        
        if note.user == request.user: # If the note is owned by the user.
            return Response(serializer.data)
        
        if request.user in note.shared_with.all(): # if the note is shared with the user.
            return Response(serializer.data)
        
        return Response({'Authorization Failed': 'Not allowed to view this note.'}, status=400)
