from django.urls import path, include
from .views import (
    RegisterView,
    GetEmailView,
    UserView,
    PasswordResetRequestView,
    PasswordResetView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('modify', UserView.as_view(), name='handle_user'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('refreshtoken', TokenRefreshView.as_view(), name='refreshtoken'),
    path('verifytoken', TokenVerifyView.as_view(), name='verifytoken'),
    path('get-email', GetEmailView.as_view(), name='get-username'),
    path('password-reset-request', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/<str:uid>/<str:token>', PasswordResetView.as_view(), name='password-reset'),
]
