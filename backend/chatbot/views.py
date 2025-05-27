# backend/chatbot/views.py

import json
import openai
from django.conf import settings
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from movies.models import Movie, TVShow

class ChatBotView(APIView):
    permission_classes = [AllowAny]

    FUNCTIONS = [
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
        }
    ]

    def post(self, request):
        user_message = request.data.get('message', '')
        openai.api_key = settings.OPENAI_API_KEY

        # 1) Function calling ile ilk çağrı
        chat_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            functions=self.FUNCTIONS,
            function_call="auto"
        )

        choice = chat_response.choices[0]
        if choice.finish_reason == "function_call":
            fn_call = choice.message.function_call
            name    = fn_call.name
            args    = json.loads(fn_call.arguments or "{}")

            # --- Eğer TVShow fonksiyonu seçilmişse, önce Movie DB'de eşleşme kontrol et ---
            if name == "get_tvshow_info":
                candidate = args.get("name", "")
                if Movie.objects.filter(title__iexact=candidate).exists():
                    # Movie DB'de var: override ederek movie fonksiyonuna geç
                    name = "get_movie_info"
                    args = {"title": candidate}

            # 2a) Film bilgisi
            if name == "get_movie_info":
                title = args.get("title", "")
                try:
                    movie = Movie.objects.get(title__iexact=title)
                except Movie.DoesNotExist:
                    return Response({
                        "response": f"Maalesef veritabanımda “{title}” filmine dair bilgi bulunmamaktadır."
                    })

                data = model_to_dict(movie, fields=[
                    "title","original_title","overview","tagline","release_date",
                    "runtime","homepage","status","original_language","budget","revenue",
                    "popularity","vote_average","vote_count","poster_path","backdrop_path",
                    "trailer_url","imdb_id","facebook_id","instagram_id","twitter_id",
                    "director"
                ])
                data["cast"]   = movie.cast or []
                data["genres"] = [g.name for g in movie.genres.all()]

            # 2b) Dizi bilgisi
            elif name == "get_tvshow_info":
                show_name = args.get("name", "")
                try:
                    show = TVShow.objects.get(name__iexact=show_name)
                except TVShow.DoesNotExist:
                    return Response({
                        "response": f"Maalesef veritabanımda “{show_name}” dizisine dair bilgi bulunmamaktadır."
                    })

                data = model_to_dict(show, fields=[
                    "name","original_name","overview","first_air_date","last_air_date",
                    "episode_run_time","number_of_seasons","number_of_episodes","homepage",
                    "status","original_language","popularity","vote_average","vote_count",
                    "poster_path","backdrop_path","trailer_url","imdb_id","facebook_id",
                    "instagram_id","twitter_id","director"
                ])
                data["cast"]   = show.cast or []
                data["genres"] = [g.name for g in show.genres.all()]

            else:
                # Beklenmeyen fonksiyon
                return Response({"response": "Üzgünüm, bunu şu an işleyemiyorum."})

            # 3) Fonksiyon sonucu ile ikinci çağrı
            second_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",     "content": user_message},
                    choice.message,
                    {
                        "role": "function",
                        "name": name,
                        "content": json.dumps(data, default=str)
                    }
                ]
            )
            answer = second_response.choices[0].message.content
            return Response({"response": answer})

        # 4) Function_call yoksa direkt AI cevabı
        return Response({"response": choice.message.content})
