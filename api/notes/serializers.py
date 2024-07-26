from rest_framework import serializers
from .models import Note
from users.serializers import UserSerializer

class NoteSerializer(serializers.ModelSerializer):
    """Note serializer."""
    class Meta:
        model = Note
        fields = '__all__'
        required_fields = ['title', 'content']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            "shared_with": {"read_only": True},
            'id': {'read_only': True},
        }
    user = UserSerializer(read_only=True)
    shared_with = UserSerializer(read_only=True, many=True)
