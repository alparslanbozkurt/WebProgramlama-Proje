import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Movie, Genre


class Command(BaseCommand):
    help = "Fetch up to MAX_PAGES pages of TMDB movies and store/update them in the local SQLite DB"

    TMDB_API_KEY = getattr(settings, "TMDB_API_KEY")
    BASE_URL     = "https://api.themoviedb.org/3"
    MAX_PAGES    = 500
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
        self.stdout.write("🔄 TMDB’den film keşfine başlıyor…")

        while page <= total_pages and page <= self.MAX_PAGES:
            data = self.fetch_json("/discover/movie", {**self.DISCOVER_PARAMS, "page": page})
            total_pages = min(data.get("total_pages", 1), self.MAX_PAGES)
            self.stdout.write(f"· Sayfa {page}/{total_pages} ({len(data['results'])} film)")

            for item in data["results"]:
                tmdb_id = item["id"]
                movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id)

                detail = self.fetch_json(
                    f"/movie/{tmdb_id}",
                    {
                        "append_to_response": "videos,credits,external_ids,similar,reviews",
                        "language": self.DISCOVER_PARAMS["language"],
                    }
                )

                # External IDs
                ext = detail.get("external_ids", {})
                movie.imdb_id      = ext.get("imdb_id")
                movie.facebook_id  = ext.get("facebook_id")
                movie.instagram_id = ext.get("instagram_id")
                movie.twitter_id   = ext.get("twitter_id")

                # Genres
                genre_objs = []
                for g in detail.get("genres", []):
                    obj, _ = Genre.objects.get_or_create(
                        tmdb_id=g["id"],
                        defaults={"name": g["name"]}
                    )
                    genre_objs.append(obj)

                # Diğer alanlar
                movie.title             = detail.get("title", "")
                movie.original_title    = detail.get("original_title") or ""
                movie.overview          = detail.get("overview") or ""
                movie.tagline           = detail.get("tagline") or ""
                movie.release_date      = detail.get("release_date") or None
                movie.runtime           = detail.get("runtime")
                movie.homepage          = detail.get("homepage") or ""
                movie.status            = detail.get("status") or ""
                movie.original_language = detail.get("original_language") or ""
                movie.budget            = detail.get("budget") or 0
                movie.revenue           = detail.get("revenue") or 0
                movie.popularity        = detail.get("popularity") or 0.0
                movie.vote_average      = detail.get("vote_average") or 0.0
                movie.vote_count        = detail.get("vote_count") or 0
                movie.poster_path       = detail.get("poster_path") or ""
                movie.backdrop_path     = detail.get("backdrop_path") or ""
                movie.save()

                movie.genres.set(genre_objs)

                status = "✔️ Oluşturuldu" if created else "🔄 Güncellendi"
                self.stdout.write(f"    {status}: {movie.title}")

            page += 1
            time.sleep(self.SLEEP_SEC)

        toplam = Movie.objects.count()
        self.stdout.write(self.style.SUCCESS(f"✅ Film çekim tamamlandı. Toplam film: {toplam}"))