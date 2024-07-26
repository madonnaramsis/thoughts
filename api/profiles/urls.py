from django.urls import path, include
from .views import Viewprofile, ProfileModifyView

urlpatterns = [
    path('<str:username>', Viewprofile.as_view(), name='profile'),
    path('<str:username>/modify', ProfileModifyView.as_view(), name='modify'),
]
