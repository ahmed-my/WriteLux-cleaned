from django.shortcuts import render
from .models import Fitness, Image, Lesson, Course
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

def course_page(request, param):
    posts = Post.objects.all()
    courses = Course.objects.all()
    course = Course.objects.get(slug=param)
    context = {
        'posts': posts,
        'courses': courses,
        'course': course
    }
    return render(request, 'fitness/course_page.html', context)