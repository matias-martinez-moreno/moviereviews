import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Add movies from image filenames'

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        for filename in os.listdir(images_folder):
            if filename.startswith('m_') and filename.endswith('.png'):
                title = filename[2:-4].replace('_', ' ')
                if not Movie.objects.filter(title=title).exists():
                    Movie.objects.create(
                        title=title,
                        description='',
                        genre='',
                        year=None
                    )
                    self.stdout.write(f"Added movie: {title}")
                else:
                    self.stdout.write(f"Movie already exists: {title}")