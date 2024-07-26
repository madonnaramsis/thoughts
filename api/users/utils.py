"""Utils functions for users app."""
from .models import User
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken

def username_generator(email: str) -> str:
    """Generate a username from an email address."""
    email_prefix = email.split('@')[0].lower()
    while User.objects.filter(username=email_prefix).exists():
        email_prefix += str(randint(0, 9))
    return email_prefix

def get_tokens_for_user(user: User) -> dict:
    """Generate tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
