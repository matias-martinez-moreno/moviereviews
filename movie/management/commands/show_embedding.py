import os
import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Show the embedding of a random movie"

    def handle(self, *args, **kwargs):
        # Select a random movie
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write(self.style.ERROR("No movies found in the database."))
            return

        random_movie = random.choice(movies)
        
        # Retrieve and decode the embedding
        try:
            embedding_vector = np.frombuffer(random_movie.emb, dtype=np.float32)
            self.stdout.write(self.style.SUCCESS(f"Embedding for random movie '{random_movie.title}':"))
            self.stdout.write(f"{embedding_vector}")
        except ValueError:
            self.stdout.write(self.style.ERROR(f"Could not decode embedding for '{random_movie.title}'."))
