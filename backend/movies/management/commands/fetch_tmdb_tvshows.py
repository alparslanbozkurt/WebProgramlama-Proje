import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import TVShow, Genre

class Command(BaseCommand):
    help = "Fetch up to MAX_PAGES pages of TMDB TV shows and store/update them in the local SQLite DB"

    TMDB_API_KEY = getattr(settings, "TMDB_API_KEY")
    BASE_URL     = "https://api.themoviedb.org/3"
    MAX_PAGES    = 100
    SLEEP_SEC    = 0.2

    DISCOVER_PARAMS = {
        "language": "en-US",
        "sort_by": "popularity.desc",
    }

    def fetch_json(self, path: str, params: dict = None) -> dict:
        p = params.copy() if params else {}
        p["api_key"] = self.TMDB_API_KEY
        resp = requests.get(f"{self.BASE_URL}{path}", params=p, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def handle(self, *args, **options):
        page, total_pages = 1, 1
        self.stdout.write("🔄 TMDB’den dizi keşfine başlıyor…")

        while page <= total_pages and page <= self.MAX_PAGES:
            data = self.fetch_json("/discover/tv", {**self.DISCOVER_PARAMS, "page": page})
            total_pages = min(data.get("total_pages", 1), self.MAX_PAGES)
            self.stdout.write(f"· Sayfa {page}/{total_pages} ({len(data['results'])} dizi)")

            for item in data["results"]:
                tmdb_id = item["id"]
                show, created = TVShow.objects.get_or_create(tmdb_id=tmdb_id)

                detail = self.fetch_json(
                    f"/tv/{tmdb_id}",
                    {
                        "append_to_response": "credits,external_ids,similar,reviews,videos",
                        "language": self.DISCOVER_PARAMS["language"],
                    }
                )

                # External IDs
                ext = detail.get("external_ids", {})
                show.imdb_id      = ext.get("imdb_id")
                show.facebook_id  = ext.get("facebook_id")
                show.instagram_id = ext.get("instagram_id")
                show.twitter_id   = ext.get("twitter_id")

                # Genres
                genre_objs = []
                for g in detail.get("genres", []):
                    obj, _ = Genre.objects.get_or_create(
                        tmdb_id=g["id"],
                        defaults={"name": g["name"]}
                    )
                    genre_objs.append(obj)

                # Trailer
                vids = detail.get("videos", {}).get("results", [])
                trailer = next(
                    (v for v in vids if v.get("type") == "Trailer" and v.get("site") == "YouTube"),
                    None
                )
                show.trailer_url = (
                    f"https://www.youtube.com/watch?v={trailer['key']}"
                    if trailer else ""
                )

                # Diğer detaylar
                show.name               = detail.get("name", "")
                show.original_name      = detail.get("original_name") or ""
                show.overview           = detail.get("overview") or ""
                show.first_air_date     = detail.get("first_air_date") or None
                show.last_air_date      = detail.get("last_air_date") or None
                runtimes = detail.get("episode_run_time", [])
                show.episode_run_time   = runtimes[0] if runtimes else None
                show.number_of_seasons  = detail.get("number_of_seasons") or 0
                show.number_of_episodes = detail.get("number_of_episodes") or 0
                show.homepage           = detail.get("homepage") or ""
                show.status             = detail.get("status") or ""
                show.original_language  = detail.get("original_language") or ""
                show.popularity         = detail.get("popularity") or 0.0
                show.vote_average       = detail.get("vote_average") or 0.0
                show.vote_count         = detail.get("vote_count") or 0
                show.poster_path        = detail.get("poster_path") or ""
                show.backdrop_path      = detail.get("backdrop_path") or ""
                credits = detail.get("credits", {})
                directors = [person["name"] for person in credits.get("crew", []) if person.get("job") == "Director"]
                show.director = ", ".join(directors) if directors else ""
                show.cast = [person["name"] for person in credits.get("cast", [])[:10]] if credits.get("cast") else []
                show.save()

                show.genres.set(genre_objs)

                flag = "✔️ Oluşturuldu" if created else "🔄 Güncellendi"
                self.stdout.write(f"    {flag}: {show.name}")

            page += 1
            time.sleep(self.SLEEP_SEC)

        total = TVShow.objects.count()
        self.stdout.write(self.style.SUCCESS(f"✅ Dizi çekim tamamlandı. Toplam dizi: {total}"))
