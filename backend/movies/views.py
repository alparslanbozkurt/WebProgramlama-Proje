from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Movie, TVShow
from .serializers import MovieSerializer, TVShowSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-popularity')
    serializer_class = MovieSerializer

    @action(detail=False, methods=['get'])
    def trending(self, request):
        top8 = self.get_queryset()[:8]
        ser = self.get_serializer(top8, many=True)
        return Response(ser.data)

class TVShowViewSet(viewsets.ModelViewSet):
    queryset = TVShow.objects.all().order_by('-popularity')
    serializer_class = TVShowSerializer

    @action(detail=False, methods=['get'])
    def trending(self, request):
        top8 = self.get_queryset()[:8]
        ser = self.get_serializer(top8, many=True)
        return Response(ser.data)