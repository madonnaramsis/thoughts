from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsProfileOwner

class Viewprofile(APIView):
    """View users profile based on username suffix."""
    permission_classes = [AllowAny]
    def get_object(self, username):
        profile = Profile.objects.get(user__username=username)
        return profile

    def get(self, request, username):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileModifyView(Viewprofile):
    """Edit profile view"""
    permission_classes = [IsProfileOwner]

    def put(self, request, username):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=202)
        return Response(serializer.errors, status=400)
