from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Dakika cinsinden")
    genres = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)
    vote_count = models.PositiveIntegerField(default=0)
    popularity = models.FloatField(default=0.0)
    trailer_url = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)

    imdb_id = models.CharField(max_length=50, blank=True)
    twitter_handle = models.CharField(max_length=100, blank=True)
    watch_platforms = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class MovieTranslation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="translations")
    language_code = models.CharField(max_length=10)
    translated_title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.language_code}: {self.translated_title}"


class MovieKeyword(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class MovieRecommendation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="base_movie")
    recommended_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="recommended")

    def __str__(self):
        return f"{self.movie.title} → {self.recommended_movie.title}"


class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="cast")
    actor_name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} as {self.character_name}"


class Crew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="crew")
    role = models.CharField(max_length=100)  # Örn: Director, Writer, Producer
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.role}"


class UserWatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} liked {self.movie.title}"
