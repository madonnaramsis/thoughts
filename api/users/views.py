from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .permissions import IsAuthenticatedUser
from .utils import username_generator, get_tokens_for_user
from django.conf import settings


class RegisterView(APIView):
    """Creating user accounts with thier profile object using signals."""
    permission_classes = [AllowAny]
    def post(self, request):
        """Creates a new user account."""
        if not request.data.get('username') and request.data.get('email'): # if username is not provided
            request.data['username'] = username_generator(request.data['email']) # generate a username
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({"tokens": tokens, "data": serializer.data}, 201)


class UserView(APIView):
    """Base class for user views."""
    permission_classes = [IsAuthenticatedUser]

    def get(self, request):
        """Get the user object."""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """Update the user object."""
        user = request.user
        
        if not user.check_password(request.data.get('password')): # if the password is incorrect
            return Response({'Authorization': 'Failed'}, status=400)
        
        if not request.data.get('username') and request.data.get('email'): # if username is not provided
            request.data['username'] = user.username # use the existing username
        
        if not request.data.get('email'): # if email is not provided
            request.data['email'] = user.email # use the existing email
        
        if request.data.get('new_password'): # if new password is provided
            request.data['password'] = request.data['new_password'] # use the new password
            request.data.pop('new_password') # remove the new password from the request data
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=202)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        """Delete the user object."""
        user = request.user
        
        if not user.check_password(request.data.get('password')):
            return Response({'Authorization': 'Wrong password'}, status=400)
        
        user.delete()
        return Response(status=204)


class PasswordResetRequestView(APIView):
    """Allow users to request a password reset."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Send an email with a password reset link."""
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"Success": "Reset email sent successfully"}, status=200)
        return Response(serializer.errors, status=400)


class PasswordResetView(APIView):
    """Allow users to reset their password."""
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        """Reset the password of the user."""
        serializer = PasswordResetSerializer(
            data=request.data,
            context={
                'uid': uid,
                'token': token,
            })
        if serializer.is_valid(raise_exception=True):
            return Response({"Success": "Password reset successfully"}, status=200)
        return Response(serializer.errors, status=400)

class GetEmailView(APIView):
    """Allow users to login with their email address."""
    permission_classes = [AllowAny]

    def get_object(self, request):
        """used to retrieve the user object."""
        username = request.data.get('username')
        return User.objects.get(username=username)

    def get(self, request):
        """Return the email of the user for the given username."""
        user = self.get_object(request=request)
        return Response(user.email, status=200)
