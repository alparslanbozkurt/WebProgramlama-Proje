from django.urls import path
from .views import movie_list, movie_detail

app_name = 'movies'
urlpatterns = [
    path('', movie_list, name='list'),
    path('<int:movie_id>/', movie_detail, name='detail'),
]