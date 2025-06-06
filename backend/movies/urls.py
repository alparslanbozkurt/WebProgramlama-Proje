from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MovieViewSet,
    TVShowViewSet,
    GenreViewSet,
    ReviewViewSet,
    MovieAITipView,
    TVShowAITipView# <—— Burada yeni view’i import edin
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'tvshows', TVShowViewSet, basename='tvshow')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    # 1) Önce tüm router tarafından oluşturulan endpoint’leri ekleyelim
    path('', include(router.urls)),

    # 2) Ardından “AI tip” endpoint’ini ekleyelim:
    path('movies/<int:pk>/ai_tip/', MovieAITipView.as_view(), name='movie-ai-tip'),
    path(
        'tvshows/<int:pk>/ai_tip/',
        TVShowAITipView.as_view(),
        name='tvshow-ai-tip'
    ),
]