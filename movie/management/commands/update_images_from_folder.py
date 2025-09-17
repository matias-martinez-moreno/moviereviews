import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Update movie images from folder'

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        for filename in os.listdir(images_folder):
            if filename.startswith('m_') and filename.endswith('.png'):
                # Extract title from filename, e.g., m_The Lion King.png -> The Lion King
                title = filename[2:-4]
                try:
                    movie = Movie.objects.get(title=title)
                    movie.image = f'movie/images/{filename}'
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                except Movie.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Movie '{title}' not found in DB for image '{filename}'"))