from rest_framework import serializers
from .models import Movie, UserWatchHistory, Comment, Like

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchHistory
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
