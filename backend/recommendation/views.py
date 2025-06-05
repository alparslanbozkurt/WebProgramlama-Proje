from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from movies.models import Movie, TVShow
from vertexai.generative_models import GenerativeModel
import vertexai
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models.functions import Lower
from django.db.models import Value, CharField
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class AIPersonalizedRecommendationView(APIView):
    """
    POST /api/ai_recommendations/
    Kullanıcının tercihini alır, AI ile film ve dizi önerir.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_pref = request.data.get("preference", "").strip()
        if not user_pref:
            return Response({"detail": "Lütfen bir tercih belirtin."}, status=400)

        # Vertex AI başlat
        vertexai.init(
            project=settings.GOOGLE_CLOUD_PROJECT_ID,
            location=settings.VERTEX_AI_REGION
        )

        model = GenerativeModel("gemini-2.0-flash-001")

        # Veritabanından başlık + içerik bilgisi (özet, tür vs.) çek
        movie_items = Movie.objects.annotate(content_type=Value("movie", output_field=CharField()))
        tv_items = TVShow.objects.annotate(content_type=Value("series", output_field=CharField()))

        all_items = list(movie_items) + list(tv_items)

        # Her bir içerik için: başlık, tür, overview gibi bilgileri topla
        content_list = []
        for item in all_items:
            title = getattr(item, "title", None) or getattr(item, "name", "")
            genres = ", ".join(g.name for g in item.genres.all()) if hasattr(item, "genres") else ""
            overview = item.overview or ""
            content_list.append(f"{title} [{item.content_type}]: Türler: {genres}. Özet: {overview}")

        # AI’a verilecek içerik listesi (kırpılabilir)
        content_input = "\n".join(content_list[:200])  # çok büyük olmasın

        # Kullanıcı dilini tespit et (çok basitçe)
        is_turkish = any(char in user_pref for char in "çğıöşüÇĞİÖŞÜ")

        if is_turkish:
            system_prompt = """
    Kullanıcıdan bir tercih cümlesi alacaksınız. Aşağıda bir veritabanı listesi var. 
    Sadece bu listedeki filmler ve dizilerden kullanıcının tercihine göre 5 film ve 5 dizi önerin.
    Her başlığın yanına neden önerdiğinizi kısaca açıklayın (tür veya içerik nedenleriyle).
    Cevabınız Türkçe olmalı.
    """
        else:
            system_prompt = """
    You will receive a user's preference sentence. Below is a database of content.
    Recommend 5 movies and 5 TV shows strictly from the list that match the preference.
    Include a short justification (genre, setting, etc.) next to each title.
    Respond in English.
    """

        final_prompt = f"""{system_prompt}

    Kullanıcı tercihi:
    "{user_pref}"

    Veritabanı içerikleri:
    {content_input}

    Yalnızca listedeki başlıklardan öneri yapın. Liste ve nedenleri şöyle yazın:
    """

        try:
            response = model.generate_content(final_prompt)
            ai_text = response.text.strip()
            logger.info(f"🧠 AI Cevabı:\n{ai_text}")

            # Başlıkları çıkar (başlık: açıklama satırlarından)
            recommended_titles = []
            for line in ai_text.splitlines():
                parts = line.split(":")[0].strip("-•– ").strip()
                if parts:
                    recommended_titles.append(parts)

            # Normalize ederek eşleşme yap
            titles_lower = [t.lower() for t in recommended_titles]

            matched_movies = Movie.objects.annotate(lower_title=Lower("title")).filter(lower_title__in=titles_lower)
            matched_series = TVShow.objects.annotate(lower_name=Lower("name")).filter(lower_name__in=titles_lower)

            serialized_movies = [{"id": m.id, "title": m.title, "type": "movie"} for m in matched_movies]
            serialized_series = [{"id": s.id, "title": s.name, "type": "series"} for s in matched_series]

            return Response({
                "ai_summary": ai_text,
                "recommendations": serialized_movies + serialized_series
            })

        except Exception as e:
            logger.error("❌ AI Hatası", exc_info=True)
            return Response({"detail": f"AI hatası: {str(e)}"}, status=500)
