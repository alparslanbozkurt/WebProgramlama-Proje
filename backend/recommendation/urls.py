from django.urls import path
from .views import (
    MovieListView, MovieDetailView, UserWatchHistoryView,
    AddCommentView, MovieCommentListView,
    LikeToggleView, MovieLikeCountView, MovieCommentCountView
)

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('history/', UserWatchHistoryView.as_view(), name='user-history'),
    path('comments/add/', AddCommentView.as_view(), name='add-comment'),
    path('comments/<int:movie_id>/', MovieCommentListView.as_view(), name='movie-comments'),
    path('like/<int:movie_id>/', LikeToggleView.as_view(), name='like-toggle'),
    path('like-count/<int:movie_id>/', MovieLikeCountView.as_view(), name='like-count'),
    path('comment-count/<int:movie_id>/', MovieCommentCountView.as_view(), name='comment-count'),
]
