from django.urls import path
from .views import RegisterView, profile

urlpatterns = [
    path('',         RegisterView.as_view(), name='auth_register'),
    path('profile/', profile,              name='auth_profile'),
]