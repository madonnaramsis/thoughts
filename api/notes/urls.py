from django.urls import path, include
from .views import NotesBaseView, NoteModifyView, SharedNotesView

urlpatterns = [
    path('<str:username>', NotesBaseView.as_view(), name='notes_base'),
    path('<str:note_id>/modify', NoteModifyView.as_view(), name='note_modify'),
    path('shared/<str:share_id>', SharedNotesView.as_view(), name='shared_notes'),
]
