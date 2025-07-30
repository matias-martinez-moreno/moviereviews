from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {'name': 'matias martinez'}  # Diccionario con el dato a pasar
    return render(request, 'home.html', context)  # Enviamos context a la plantilla

def about(request):
    return HttpResponse("This is the About Page")
