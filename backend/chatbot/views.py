import json
import openai
from django.conf import settings
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from movies.models import Movie, TVShow


class ChatBotView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    FUNCTIONS = [
        # --- Film detay fonksiyonu ---
        {
            "name": "get_movie_info",
            "description": "Veritabanındaki bir film hakkında tüm detayları döner",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Filmin başlığı"}
                },
                "required": ["title"]
            }
        },
        # --- Dizi detay fonksiyonu ---
        {
            "name": "get_tvshow_info",
            "description": "Veritabanındaki bir dizi hakkında tüm detayları döner",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Dizinin adı"}
                },
                "required": ["name"]
            }
        },
        # --- Tür bazlı öneri fonksiyonu ---
        {
            "name": "recommend_movies",
            "description": "Verilen türe göre en popüler filmleri listeler",
            "parameters": {
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "Öneri istediğiniz film türü (örneğin Horror, Comedy)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Kaç adet öneri isteniyor",
                        "default": 5
                    }
                },
                "required": ["genre"]
            }
        }
    ]

    def post(self, request):
        user_message = request.data.get('message', '')
        openai.api_key = settings.OPENAI_API_KEY

        # 1) İlk çağrı: function_call için
        chat_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            functions=self.FUNCTIONS,
            function_call="auto"
        )
        choice = chat_response.choices[0]

        # 2) Eğer fonksiyon çağırıldıysa
        if choice.finish_reason == "function_call":
            fn_call = choice.message.function_call
            name    = fn_call.name
            args    = json.loads(fn_call.arguments or "{}")

            # --- TVShow çağrısında önce Movie kontrolu ---
            if name == "get_tvshow_info":
                cand = args.get("name", "")
                if Movie.objects.filter(title__iexact=cand).exists():
                    name = "get_movie_info"
                    args = {"title": cand}

            # --- Film bilgisi ---
            if name == "get_movie_info":
                title = args.get("title", "")
                try:
                    movie = Movie.objects.get(title__iexact=title)
                except Movie.DoesNotExist:
                    return Response({"response": f"Maalesef veritabanımda “{title}” filmine dair bilgi bulunmamaktadır."})

                data = model_to_dict(movie, fields=[
                    "title","original_title","overview","tagline","release_date",
                    "runtime","homepage","status","original_language","budget","revenue",
                    "popularity","vote_average","vote_count","poster_path","backdrop_path",
                    "trailer_url","imdb_id","facebook_id","instagram_id","twitter_id",
                    "director"
                ])
                data["cast"]   = movie.cast or []
                data["genres"] = [g.name for g in movie.genres.all()]

            # --- Dizi bilgisi ---
            elif name == "get_tvshow_info":
                show_name = args.get("name", "")
                try:
                    show = TVShow.objects.get(name__iexact=show_name)
                except TVShow.DoesNotExist:
                    return Response({"response": f"Maalesef veritabanımda “{show_name}” dizisine dair bilgi bulunmamaktadır."})

                data = model_to_dict(show, fields=[
                    "name","original_name","overview","first_air_date","last_air_date",
                    "episode_run_time","number_of_seasons","number_of_episodes","homepage",
                    "status","original_language","popularity","vote_average","vote_count",
                    "poster_path","backdrop_path","trailer_url","imdb_id","facebook_id",
                    "instagram_id","twitter_id","director"
                ])
                data["cast"]   = show.cast or []
                data["genres"] = [g.name for g in show.genres.all()]

            # --- Tür bazlı film önerisi ---
            elif name == "recommend_movies":
                genre = args.get("genre", "").strip()
                count = args.get("count", 5) or 5
                # Veritabanından filtrele
                qs = (
                    Movie.objects
                    .filter(genres__name__iexact=genre)
                    .order_by('-popularity')[:count]
                )
                recommendations = []
                for m in qs:
                    recommendations.append({
                        "title": m.title,
                        "overview": m.overview,
                        "release_year": m.release_date.year if m.release_date else None,
                        "poster_path": m.poster_path,
                        "vote_average": m.vote_average
                    })
                data = {
                    "genre": genre,
                    "recommendations": recommendations
                }

            else:
                return Response({"response": "Üzgünüm, bu isteği işleyemiyorum."})

            # 3) Fonksiyon sonucu ile ikinci çağrı
            second_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",        "content": user_message},
                    choice.message,  # assistant’ın function_call
                    {
                        "role": "function",
                        "name": name,
                        "content": json.dumps(data, default=str)
                    }
                ]
            )
            answer = second_response.choices[0].message.content
            return Response({"response": answer})

        # 4) Hiç fonksiyon çağrılmadıysa: sadece DB’dekiler hakkında bilgi ver
        return Response({
            "response": "Üzgünüm, yalnızca veritabanımda kayıtlı film ve diziler hakkında bilgi verebilirim."
        })
