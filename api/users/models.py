from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from common.models import BaseModel

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Customized user model."""
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_staff(self):
        return self.is_superuser
    @is_staff.setter
    def is_staff(self, value):
        self.is_superuser = value
