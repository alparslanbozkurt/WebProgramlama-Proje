# thirdPartyLib/services/tmdb.py
import requests
from django.conf import settings

API_KEY = settings.TMDB_API_KEY
BASE_URL = settings.TMDB_API_BASE_URL

def get_popular_movies(page=1):
    """Popüler filmleri getirir."""
    url = f"{BASE_URL}/movie/popular"
    params = {'api_key': API_KEY, 'language': 'tr-TR', 'page': page}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()['results']

def get_movie_details(movie_id):
    """Tek bir filmin detaylarını getirir (açıklama, fragman, vb.)."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'tr-TR',
        'append_to_response': 'videos'  # trailer’ları da çekmek için
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()
