from openai import OpenAI
import os
import numpy as np
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Generate embeddings for movies'

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_embedding(text):
            response = client.embeddings.create(input=[text], model="text-embedding-3-small")
            return np.array(response.data[0].embedding, dtype=np.float32)

        movies = Movie.objects.all()
        for movie in movies:
            if movie.description and movie.description.strip():
                emb = get_embedding(movie.description)
                movie.emb = emb.tobytes()
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Embedding stored for: {movie.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping '{movie.title}' due to empty description."))

        self.stdout.write('Finished generating embeddings for all movies')