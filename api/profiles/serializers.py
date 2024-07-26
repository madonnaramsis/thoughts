from rest_framework import serializers
from .models import Profile
from users.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer."""
    class Meta:
        model = Profile
        fields = ['user',
                  'created_at',
                  'updated_at',
                  'first_name',
                  'last_name',
                  'bio',
                  'birth_date',
                  'avatar']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    user = UserSerializer()
