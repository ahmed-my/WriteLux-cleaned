from django.shortcuts import render
from .models import Fitness, Image

# Create your views here.
def fitness_items(request):
    fitness = Fitness.objects.all()
    return render(request, 'fitness/fitness_items.html', {'new_fitness': fitness})
