from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Genre, Movie, TVShow, Review
from rest_framework import generics

from .serializers import (
    GenreSerializer,
    MovieSerializer,
    MovieDetailSerializer,
    TVShowSerializer,
    TVShowDetailSerializer,
    GenreSerializer,
    ReviewSerializer
)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-popularity')

    def get_serializer_class(self):
        # /movies/<id>/ ise detay serializer, değilse kısa serializer
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    @action(detail=False, methods=['get'])
    def trending(self, request):
        top8 = self.get_queryset()[:200]
        ser = self.get_serializer(top8, many=True)
        return Response(ser.data)

class TVShowViewSet(viewsets.ModelViewSet):
    queryset = TVShow.objects.all().order_by('-popularity')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TVShowDetailSerializer
        return TVShowSerializer

    @action(detail=False, methods=['get'])
    def trending(self, request):
        top8 = self.get_queryset()[:200]
        ser = self.get_serializer(top8, many=True)
        return Response(ser.data)

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer

class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment', 'user__username']
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        movie_id = self.request.query_params.get('movie', None)
        tvshow_id = self.request.query_params.get('tvshow', None)
        if movie_id is not None:
            qs = qs.filter(movie_id=movie_id)
        if tvshow_id is not None:
            qs = qs.filter(tvshow_id=tvshow_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)