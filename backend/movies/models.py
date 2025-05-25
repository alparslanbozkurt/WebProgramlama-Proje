from django.db import models

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id         = models.IntegerField(unique=True)
    title           = models.CharField(max_length=255)
    original_title  = models.CharField(max_length=255, blank=True, null=True)
    overview        = models.TextField(blank=True)
    tagline         = models.CharField(max_length=255, blank=True)
    release_date    = models.DateField(blank=True, null=True)
    runtime         = models.IntegerField(blank=True, null=True)
    homepage        = models.URLField(blank=True)
    status          = models.CharField(max_length=50, blank=True)
    original_language = models.CharField(max_length=10, blank=True)
    budget          = models.BigIntegerField(blank=True, null=True)
    revenue         = models.BigIntegerField(blank=True, null=True)
    popularity      = models.FloatField(default=0.0)
    vote_average    = models.FloatField(default=0.0)
    vote_count      = models.IntegerField(default=0)
    poster_path     = models.CharField(max_length=200, blank=True)
    backdrop_path   = models.CharField(max_length=200, blank=True)
    genres          = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return f"{self.title} ({self.release_date})"