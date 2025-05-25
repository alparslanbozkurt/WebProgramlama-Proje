from rest_framework import serializers
from .models import Movie, TVShow
from movies.services.auth_service import AuthService

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

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return AuthService.register_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = AuthService.verify_credentials(
            username=data['username'],
            password=data['password']
        )
        return {'user_id': user.id, 'username': user.username}