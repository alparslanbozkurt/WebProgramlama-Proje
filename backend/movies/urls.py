from django.urls import path
from .api import trending_movies, trending_series

urlpatterns = [
    path("trending/movies/", trending_movies, name="trending-movies"),
    path("trending/series/", trending_series, name="trending-series"),
]
