from django.urls import path
from .api import trending_movies, trending_series
from movies.views import RegisterView, LoginView

urlpatterns = [
    path("trending/movies/", trending_movies, name="trending-movies"),
    path("trending/series/", trending_series, name="trending-series"),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]
