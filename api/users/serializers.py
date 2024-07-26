from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    def validate_username(self, value):
        """Ensure username does not contain '@'."""
        if '@' in value:
            raise serializers.ValidationError("Username cannot contain '@'.")
        return value

    def validate_password(self, value):
        """Ensure password is at least 8 characters long."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Called from .save() method in the view to create a new user."""
        # We don't have to hash it here because the password is hashed in the model.
        user = User.objects.create_user(**validated_data)
        send_mail(
            'Welcome to Thoughts!',
            'You have successfully created an account on our platform.',
            "no-reply_thoughts@ku18m.tech",
            [user.email],
            fail_silently=False,
            )
        return user

    def update(self, instance, validated_data):
        """Called from .save() method in the view to update the user."""
        if validated_data.get('password'):
            # Hash the password before saving it.
            validated_data['password'] = make_password(validated_data.get('password'))
        send_mail(
            'Your account has been updated!',
            'You have successfully updated your Thoughts account.',
            "no-reply_thoughts@ku18m.tech",
            [instance.email],
            fail_silently=False,
            )
        return super().update(instance, validated_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer."""
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://localhost:8000/users/password-reset/{uid}/{token}"
            send_mail(
            'Password Reset Request',
            'Click the link below to reset your password.\n' + link,
            "no-reply_thoughts@ku18m.tech",
            [email],
            fail_silently=False,
            )
        else:
            raise serializers.ValidationError("User with this email does not exist.")
        return super().validate(attrs)


class PasswordResetSerializer(serializers.Serializer):
    """Password reset serializer."""
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid token.")
        user.set_password(password)
        user.save()
        send_mail(
            'Password Reset Successful',
            'You have successfully reset your password.',
            "no-reply_thoughts@ku18m.tech",
            [user.email],
            fail_silently=False,
        )
        return attrs

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """Customizes the token response payload."""
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['id'] = str(user.id) # Because the id is an instance of UUID object.
        
        # In case we dicided to add first_name and last_name to the token payload.
        # token['first_name'] = user.first_name
        # token['last_name'] = user.last_name

        return token
