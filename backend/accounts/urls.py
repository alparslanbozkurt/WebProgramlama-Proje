from django.urls import path
from .views import RegisterView, LoginView, LogoutView, csrf_token, MeView

urlpatterns = [
    path('csrf/',     csrf_token,           name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('me/',       MeView.as_view(),       name='me'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
]
