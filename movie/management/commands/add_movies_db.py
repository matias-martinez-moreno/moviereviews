from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        json_file_path = 'movie/management/commands/movies.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)
        
        # Add movies to the database
        count = 0
        for i in range(min(100, len(movies))):
            movie = movies[i]
            exist = Movie.objects.filter(title=movie['title']).first()
            if not exist:
                try:              
                    Movie.objects.create(
                        title=movie['title'],
                        image='movies/images/default.jpg',
                        genre=movie.get('genre', ''),
                        year=movie.get('year'),
                        description=movie.get('plot', ''),
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(f"Error creating movie {movie.get('title', 'Unknown')}: {e}")
            else:
                try:
                    exist.title = movie["title"]
                    exist.image = 'movies/images/default.jpg'
                    exist.genre = movie.get("genre", "")
                    exist.year = movie.get("year")
                    exist.description = movie.get("plot", "")
                    exist.save()
                    count += 1
                except Exception as e:
                    self.stdout.write(f"Error updating movie {movie.get('title', 'Unknown')}: {e}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} movies'))
