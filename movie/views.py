from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie, Subscription
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    searchTerm = request.GET.get('searchMovie')
    genreFilter = request.GET.get('genre')
    yearFilter = request.GET.get('year')
    
    movies = Movie.objects.all()
    
    # Aplicar filtros
    if searchTerm:
        movies = movies.filter(title__icontains=searchTerm)
    
    if genreFilter:
        movies = movies.filter(genre=genreFilter)
    
    if yearFilter:
        # Filtrar por década
        if yearFilter == '1990':
            movies = movies.filter(year__gte=1990, year__lt=2000)
        elif yearFilter == '2000':
            movies = movies.filter(year__gte=2000, year__lt=2010)
        elif yearFilter == '2010':
            movies = movies.filter(year__gte=2010, year__lt=2020)
        elif yearFilter == '2020':
            movies = movies.filter(year__gte=2020)
    
    return render(request, 'home.html', {
        'name': 'Matías Martínez', 
        'movies': movies,
        'current_search': searchTerm,
        'current_genre': genreFilter,
        'current_year': yearFilter
    })

def about(request):
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    # Filtrar las películas por año y género y contar la cantidad
    for movie in all_movies:
        # Contar por año
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
        
        # Contar por género (solo el primer género)
        genre = movie.genre if movie.genre else "None"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    # Crear gráfica de películas por año
    plt.figure(figsize=(12, 6))
    
    # Gráfica de año
    plt.subplot(1, 2, 1)
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center', color='#495057')
    plt.title('Movies per Year', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=45)
    plt.grid(True, alpha=0.3)

    # Gráfica de género
    plt.subplot(1, 2, 2)
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='#ffc107')
    plt.title('Movies per Genre', fontsize=14, fontweight='bold')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=45)
    plt.grid(True, alpha=0.3)

    # Ajustar el espaciado
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            try:
                # Verificar si ya existe
                subscription, created = Subscription.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                
                if created:
                    messages.success(request, f'Successfully subscribed with {email}!')
                else:
                    if subscription.is_active:
                        messages.info(request, f'{email} is already subscribed.')
                    else:
                        subscription.is_active = True
                        subscription.save()
                        messages.success(request, f'Re-activated subscription for {email}!')
                        
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
            
            return redirect('home')
    
    # Si es GET, mostrar la página de signup
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email})

def login(request):
    return render(request, 'login.html')
