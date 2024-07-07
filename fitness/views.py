from django.shortcuts import render
from .models import Fitness, Image, Lesson
from posts.models import Post

# Create your views here.
def fitness_items(request):
    fitness = Fitness.objects.all()
    return render(request, 'fitness/fitness_items.html', {'fitness': fitness})

def lesson_page(request, param):
    posts = Post.objects.all()
    lessons = Lesson.objects.all()
    lesson = Lesson.objects.get(slug=param)
    context = {
        'posts': posts,
        'lessons': lessons,
        'lesson': lesson
    }
    return render(request, 'fitness/lesson_page.html', context)