from django.contrib import admin
from django.urls import path, include


from core.views import RegisterView, MyTokenObtainPairView, profile
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(),              name='auth_register'),
    path('api/auth/login/',    MyTokenObtainPairView.as_view(),     name='token_obtain_pair'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(),          name='token_refresh'),
    path('api/auth/logout/',   TokenBlacklistView.as_view(),        name='token_blacklist'),
    path('api/auth/profile/',  profile,                             name='profile'),

    path('api/movies/',        include('movies.urls')),
    path('api/recommendation/',include('recommendation.urls')),
]
