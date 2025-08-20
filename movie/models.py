from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/images', null=True, blank=True)
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
