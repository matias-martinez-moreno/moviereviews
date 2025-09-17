from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Calculate movie similarities using embeddings'

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_embedding(text):
            response = client.embeddings.create(input=[text], model="text-embedding-3-small")
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # Select two movies
        try:
            movie1 = Movie.objects.get(title="Interstellar")
            movie2 = Movie.objects.get(title="The Godfather")
        except Movie.DoesNotExist as e:
            self.stdout.write(f"Movie not found: {e}")
            return

        # Calculate similarity between two movies
        emb1 = np.frombuffer(movie1.emb, dtype=np.float32)
        emb2 = np.frombuffer(movie2.emb, dtype=np.float32)
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")

        # Calculate similarity with prompt
        prompt = "película sobre la Segunda Guerra Mundial"
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")

        # Find best match for prompt
        best_movie = None
        max_similarity = -1
        for movie in Movie.objects.all():
            movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
            similarity = cosine_similarity(prompt_emb, movie_emb)
            if similarity > max_similarity:
                max_similarity = similarity
                best_movie = movie

        self.stdout.write(f"La película más similar al prompt '{prompt}' es: {best_movie.title} con similitud {max_similarity:.4f}")

        # Show embedding for a random movie
        import random
        random_movie = random.choice(list(Movie.objects.all()))
        random_emb = np.frombuffer(random_movie.emb, dtype=np.float32)
        self.stdout.write(f"Embedding for random movie '{random_movie.title}': {random_emb[:5]}... (first 5 values)")