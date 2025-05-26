from django.db import models
from django.contrib.auth.models import AbstractUser

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    homepage = models.URLField(blank=True)
    status = models.CharField(max_length=50, blank=True)
    original_language = models.CharField(max_length=10, blank=True)
    budget = models.BigIntegerField(blank=True, null=True)
    revenue = models.BigIntegerField(blank=True, null=True)
    popularity = models.FloatField(default=0.0)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    poster_path = models.CharField(max_length=200, blank=True)
    backdrop_path = models.CharField(max_length=200, blank=True)
    trailer_url = models.URLField(blank=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    instagram_id = models.CharField(max_length=100, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return f"{self.title} ({self.release_date})"


class TVShow(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    first_air_date = models.DateField(blank=True, null=True)
    last_air_date = models.DateField(blank=True, null=True)
    episode_run_time = models.IntegerField(blank=True, null=True,
                                           help_text="Ort. bölüm süresi (dakika)")
    number_of_seasons = models.IntegerField(default=0)
    number_of_episodes = models.IntegerField(default=0)
    homepage = models.URLField(blank=True)
    status = models.CharField(max_length=50, blank=True)
    original_language = models.CharField(max_length=10, blank=True)
    popularity = models.FloatField(default=0.0)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    poster_path = models.CharField(max_length=200, blank=True)
    backdrop_path = models.CharField(max_length=200, blank=True)
    # Yeni sosyal / IMDb alanları
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    instagram_id = models.CharField(max_length=100, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="tvshows")

    def __str__(self):
        return f"{self.name} ({self.first_air_date})"

