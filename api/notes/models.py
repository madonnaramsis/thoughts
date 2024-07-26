from common.models import BaseModel
from django.db import models
from uuid import uuid4

class Note(BaseModel):
    """Note model."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE) # User who created the note.
    is_public_shared = models.BooleanField(default=False) # Public sharing indicator.
    share_id = models.UUIDField(unique=True, default=uuid4, editable=False) # For public sharing it'll be the suffix.
    shared_with = models.ManyToManyField('users.User', related_name='shared_notes') # For specifeid users sharing.
