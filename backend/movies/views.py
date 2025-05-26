from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, TVShow
from .serializers import (
    MovieSerializer,
    MovieDetailSerializer,
    TVShowSerializer,
    TVShowDetailSerializer,
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
        top8 = self.get_queryset()[:8]
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
        top8 = self.get_queryset()[:8]
        ser = self.get_serializer(top8, many=True)
        return Response(ser.data)
