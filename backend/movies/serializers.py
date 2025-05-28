from django.db.models import Count, Q
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

class SimilarTVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = ['id', 'name', 'poster_path', 'first_air_date', 'vote_average']

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
        # Ana filmin genre ID'leri
        main_genre_ids = obj.genres.values_list('id', flat=True)
        # Kendisini hariç tut, ortak genre sayısına göre sırala, ilk 5
        queryset = (
            Movie.objects
            .exclude(id=obj.id)
            .annotate(same_genre_count=Count('genres', filter=Q(genres__in=main_genre_ids), distinct=True))
            .filter(same_genre_count__gt=0)
            .order_by('-same_genre_count', '-popularity')[:5]
        )
        return SimilarMovieSerializer(queryset, many=True).data
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
        main_genre_ids = obj.genres.values_list('id', flat=True)
        queryset = (
            TVShow.objects
            .exclude(id=obj.id)
            .annotate(same_genre_count=Count('genres', filter=Q(genres__in=main_genre_ids), distinct=True))
            .filter(same_genre_count__gt=0)
            .order_by('-same_genre_count', '-popularity')[:5]
        )
        return SimilarTVShowSerializer(queryset, many=True).data


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

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'tmdb_id', 'name']