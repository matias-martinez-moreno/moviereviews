from openai import OpenAI
import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Update movie descriptions using OpenAI API'

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_completion(prompt, model="gpt-3.5-turbo"):
            messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
            )
            return response.choices[0].message.content.strip()

        instruction = "Genera una descripción corta, atractiva y detallada para la película."
        movies = Movie.objects.filter(description="")
        for movie in movies:
            prompt = f"{instruction} Título: '{movie.title}'"
            response = get_completion(prompt)
            movie.description = response
            # Asignar género y año genéricos si están vacíos
            if not movie.genre:
                movie.genre = "Unknown"
            if not movie.year:
                movie.year = 2024 # O un año por defecto
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Updated description for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS('Finished updating empty descriptions.'))