from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/images', null=True, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
