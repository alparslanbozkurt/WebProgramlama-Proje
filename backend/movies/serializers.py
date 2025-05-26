from rest_framework import serializers
from .models import Movie, TVShow, Genre

# Genre isimlerini düz string liste olarak dönecek yardımcı serializer
class GenreNameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

# Benzer filmler için basit serializer
class SimilarMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_path', 'release_date', 'vote_average']

# MOVIE DETAIL
class MovieDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    trailerUrl = serializers.CharField(source="trailer_url")
    similarMovies = serializers.SerializerMethodField()
    imdb_id = serializers.CharField()
    facebook_id = serializers.CharField()
    instagram_id = serializers.CharField()
    twitter_id = serializers.CharField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "tmdb_id",
            "title",
            "overview",
            "release_date",
            "runtime",
            "poster_path",
            "backdrop_path",
            "popularity",
            "vote_average",
            "genres",
            "director",
            "cast",
            "trailerUrl",
            "similarMovies",
            "imdb_id", "facebook_id", "instagram_id", "twitter_id",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]

    def get_director(self, obj):
        # Eğer modelde director field'ı varsa onu döndür
        if hasattr(obj, "director") and obj.director:
            return obj.director
        # Eğer credits json var ise oradan çek
        if hasattr(obj, "credits") and obj.credits:
            crew = obj.credits.get("crew", [])
            directors = [c["name"] for c in crew if c.get("job") == "Director"]
            return ", ".join(directors)
        return ""

    def get_cast(self, obj):
        # Eğer modelde cast field'ı varsa onu döndür
        if hasattr(obj, "cast") and obj.cast:
            return obj.cast
        # Eğer credits json var ise oradan çek
        if hasattr(obj, "credits") and obj.credits:
            return [c["name"] for c in obj.credits.get("cast", [])[:10]]
        return []

    def get_similarMovies(self, obj):
        # Eğer benzer filmler M2M olarak tutuluyorsa
        if hasattr(obj, "similar_movies") and obj.similar_movies.exists():
            return SimilarMovieSerializer(obj.similar_movies.all(), many=True).data
        # Eğer json/text field ise
        if hasattr(obj, "similar_movies_json") and obj.similar_movies_json:
            return obj.similar_movies_json
        return []

# TVSHOW DETAIL
class TVShowDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    trailerUrl = serializers.CharField(source="trailer_url")
    similarShows = serializers.SerializerMethodField()
    imdb_id = serializers.CharField()
    facebook_id = serializers.CharField()
    instagram_id = serializers.CharField()
    twitter_id = serializers.CharField()

    class Meta:
        model = TVShow
        fields = [
            "id",
            "tmdb_id",
            "name",
            "overview",
            "first_air_date",
            "last_air_date",
            "episode_run_time",
            "poster_path",
            "backdrop_path",
            "popularity",
            "vote_average",
            "genres",
            "director",
            "cast",
            "trailerUrl",
            "similarShows",
            "imdb_id", "facebook_id", "instagram_id", "twitter_id",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]

    def get_director(self, obj):
        if hasattr(obj, "director") and obj.director:
            return obj.director
        if hasattr(obj, "credits") and obj.credits:
            crew = obj.credits.get("crew", [])
            directors = [c["name"] for c in crew if c.get("job") == "Director"]
            return ", ".join(directors)
        return ""

    def get_cast(self, obj):
        if hasattr(obj, "cast") and obj.cast:
            return obj.cast
        if hasattr(obj, "credits") and obj.credits:
            return [c["name"] for c in obj.credits.get("cast", [])[:10]]
        return []

    def get_similarShows(self, obj):
        if hasattr(obj, "similar_shows") and obj.similar_shows.exists():
            return SimilarMovieSerializer(obj.similar_shows.all(), many=True).data
        if hasattr(obj, "similar_shows_json") and obj.similar_shows_json:
            return obj.similar_shows_json
        return []

# Kısa liste için olanlar, aynı kalsın:
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id","tmdb_id", "title", "overview", "release_date",
            "poster_path", "popularity", "vote_average",
        ]

class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = [
            "id","tmdb_id", "name", "overview", "first_air_date",
            "poster_path", "popularity", "vote_average",
        ]
