# thirdPartyLib/views.py
from django.shortcuts import render, get_object_or_404
from .services.tmdb import get_popular_movies, get_movie_details

def movie_list(request):
    # sayfa parametresi ?page=2 gibi gelecekse al
    page = request.GET.get('page', 1)
    movies = get_popular_movies(page=page)
    return render(request, 'thirdPartyLib/movie_list.html', {
        'movies': movies,
        'page': int(page),
    })

def movie_detail(request, movie_id):
    movie = get_movie_details(movie_id)
    return render(request, 'thirdPartyLib/movie_detail.html', {
        'movie': movie,
    })
