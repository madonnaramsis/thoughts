from django.db import models
from common.models import BaseModel

# Create your models here.
class Profile(BaseModel):
    """Profile model."""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.CharField(max_length=255, default='default')
