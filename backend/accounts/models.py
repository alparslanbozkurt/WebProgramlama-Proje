from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from movies.models import Genre, Movie, TVShow


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # Bildirim tercihleri (örnek: {"email": true, "sms": false})
    notification_preferences = models.JSONField(default=dict, blank=True)

    # Favori türler (ManyToMany → kullanıcı birçok tür seçebilir)
    favorite_genres = models.ManyToManyField(Genre, blank=True)

    # Override group and permission relations to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_permissions'
    )

    def __str__(self):
        return self.username

class WatchHistory(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, null=True, blank=True)
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(help_text="İzlenen süre (dakika)")

    def __str__(self):
        return f"{self.user.username} watched {self.movie or self.tv_show}"

class WatchlistItem(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.movie or self.tv_show}"
