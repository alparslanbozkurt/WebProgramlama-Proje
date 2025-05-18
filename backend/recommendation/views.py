from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, UserWatchHistory, Comment, Like
from .serializers import (
    MovieSerializer,
    WatchHistorySerializer,
    CommentSerializer,
    LikeSerializer
)
from django.shortcuts import get_object_or_404
from django.db.models import Count


# Tüm filmleri listele
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


# Tekil film detaylarını getir
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


# Kullanıcının izleme geçmişi
class UserWatchHistoryView(generics.ListAPIView):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWatchHistory.objects.filter(user=self.request.user)


# Yorum ekle
class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Belirli bir film için yorumları getir
class MovieCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Comment.objects.filter(movie_id=movie_id)


# Beğeni ekle / kaldır
class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        like, created = Like.objects.get_or_create(user=request.user, movie=movie)
        if not created:
            # Beğeni zaten varsa, kaldır (toggle)
            like.delete()
            return Response({'message': 'Beğeni kaldırıldı'}, status=status.HTTP_200_OK)
        return Response({'message': 'Beğeni eklendi'}, status=status.HTTP_201_CREATED)


# Beğeni sayısını getir
class MovieLikeCountView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, movie_id):
        count = Like.objects.filter(movie_id=movie_id).count()
        return Response({'movie_id': movie_id, 'like_count': count})


#Yorum sayısını getir
class MovieCommentCountView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, movie_id):
        count = Comment.objects.filter(movie_id=movie_id).count()
        return Response({'movie_id': movie_id, 'comment_count': count})
