from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, TVShow
from .serializers import MovieSerializer, TVShowSerializer

@api_view(["GET"])
def trending_movies(request):
    top_n = int(request.GET.get("limit", 4))
    qs = Movie.objects.order_by("-popularity")[:top_n]
    ser = MovieSerializer(qs, many=True, context={"request": request})
    return Response(ser.data)

@api_view(["GET"])
def trending_series(request):
    top_n = int(request.GET.get("limit", 4))
    qs = TVShow.objects.order_by("-popularity")[:top_n]
    ser = TVShowSerializer(qs, many=True, context={"request": request})
    return Response(ser.data)
