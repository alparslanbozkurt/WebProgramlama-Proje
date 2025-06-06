from django.urls import path
from .views import FavoriteGenresView, RegisterView, LoginView, LogoutView, csrf_token, MeView, upload_profile_picture

urlpatterns = [
    path('csrf/',     csrf_token,           name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('me/',       MeView.as_view(),       name='me'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
    path('upload-profile-picture/', upload_profile_picture, name='upload-profile-picture'),
    path('favorite-genres/', FavoriteGenresView.as_view(), name='favorite-genres'),
]
