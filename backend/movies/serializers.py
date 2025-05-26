from rest_framework import serializers
from .models import Movie, TVShow


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "tmdb_id", "title", "overview", "release_date",
            "poster_path", "popularity", "vote_average",
        ]

class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = [
            "tmdb_id", "name", "overview", "first_air_date",
            "poster_path", "popularity", "vote_average",
        ]
