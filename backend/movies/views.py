from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Genre, Movie, TVShow, Review
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from google.cloud import aiplatform
from django.conf import settings
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from google.api_core.client_options import ClientOptions
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
from vertexai.language_models import TextGenerationModel
import vertexai
from vertexai.generative_models import GenerativeModel
vertexai.init(
    project="webproje-462013",
    location="us-central1"
)

class MovieAITipView(APIView):
    """
    GET /api/movies/{id}/ai_tip/
    Film ID'sine göre yorumları alıp Google Vertex AI (Gemini 2.0) ile
    kısa bir öneri (summary) üretir.
    """

    def get(self, request, pk, format=None):
        # 1) Filmi getir
        movie = get_object_or_404(Movie, pk=pk)

        # 2) Yorumları al
        reviews_qs = Review.objects.filter(movie=movie).order_by('-created_at')
        comments = [r.comment for r in reviews_qs if r.comment and r.comment.strip()]
        if not comments:
            return Response(
                {"ai_tip": "Henüz yorum bulunamadı, bu film hakkında veri yetersiz."},
                status=status.HTTP_200_OK
            )

        # 3) Yorumları birleştir
        combined_text = " ".join(comments)
        if len(combined_text) > 5000:
            combined_text = combined_text[:5000]

        try:
            # 4) Vertex AI başlat
            vertexai.init(
                project=settings.GOOGLE_CLOUD_PROJECT_ID,
                location=settings.VERTEX_AI_REGION
            )

            # 5) Gemini 2.0 modelini yükle
            model = GenerativeModel("gemini-2.0-flash-001")

            # 6) Prompt hazırla
            prompt = (
                "Aşağıdaki kullanıcı yorumlarını okuyup, kısa bir özet şeklinde "
                "‘neler hissediliyor, genel kanaat nedir?’ tarzında bir metin oluştur.\n\n"
                "Kullanıcı Yorumları:\n"
                f"{combined_text}\n\n"
                "Özet (Türkçe):"
            )

            # 7) AI'dan yanıt al
            response = model.generate_content(prompt)

            generated_text = response.text.strip()

            return Response({"ai_tip": generated_text}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"ai_tip": f"AI önerisi alınırken bir hata oluştu: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TVShowAITipView(APIView):
    """
    GET /api/tvshows/<tvshow_id>/ai_tip/
    Bu endpoint, diziye ait yorumları alıp Google Vertex AI Gemini 2.0 ile
    kısa bir özet ve öneri ("AI tip") üretir.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, tvshow_id, format=None):
        # 1) TV Show kontrolü
        tvshow = get_object_or_404(TVShow, pk=tvshow_id)

        # 2) Yorumları çek
        reviews_qs = Review.objects.filter(tvshow=tvshow).order_by("-created_at")
        comments = [r.comment for r in reviews_qs if r.comment and r.comment.strip()]
        if not comments:
            return Response(
                {"ai_tip": "Bu diziye dair henüz yorum yok, AI önerisi oluşturulamıyor."},
                status=status.HTTP_200_OK
            )

        # 3) Yorumları birleştir
        joined_text = "\n".join(
            [f"{r.user.username}: {r.comment}" for r in reviews_qs]
        )
        if len(joined_text) > 5000:
            joined_text = joined_text[:5000]

        # 4) Vertex AI başlat
        try:
            vertexai.init(
                project=settings.GOOGLE_CLOUD_PROJECT_ID,
                location=settings.VERTEX_AI_REGION
            )

            # 5) Modeli yükle
            model = GenerativeModel("gemini-2.0-flash-001")

            # 6) Prompt oluştur
            prompt = f"""
Aşağıda bu diziye ait kullanıcı yorumları listelenmiştir. Lütfen bu yorumları dikkate alarak:
“Sizce bu diziyi izleyenlerin çoğu ne düşünüyor? Kısa ve net bir özet oluşturun. Ayrıca dizi hakkında genel bir tavsiye (AI tip) yazın.”
Kullanıcı Görüşleri:
{joined_text}
"""

            # 7) Yanıt al
            response = model.generate_content(prompt)
            ai_tip_text = response.text.strip()

            return Response({"ai_tip": ai_tip_text}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"ai_tip": f"AI özet oluşturulurken hata oluştu: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )