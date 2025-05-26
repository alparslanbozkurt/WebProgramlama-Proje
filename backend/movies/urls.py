from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, TVShowViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'tvshows', TVShowViewSet, basename='tvshow')

# router.urls zaten bir liste, direkt return edebiliriz
urlpatterns = router.urls