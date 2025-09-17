from openai import OpenAI
import os
import csv
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Update movie descriptions using OpenAI API and export to CSV'

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

        instruction = "Actualiza la descripción de la película para que sea más atractiva y detallada."
        movies = Movie.objects.all()

        # Open CSV file for writing
        with open('updated_movie_descriptions.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Updated Description'])  # Header

            for movie in movies:
                prompt = f"{instruction} Actualiza la descripción '{movie.description}' de la película '{movie.title}'"
                response = get_completion(prompt)
                writer.writerow([movie.title, response])
                self.stdout.write(self.style.SUCCESS(f"Processed: {movie.title}"))

        self.stdout.write(self.style.SUCCESS('Finished generating CSV with updated descriptions'))