from django.shortcuts import render, get_object_or_404
from .models import Fitness, Image, Lesson, Course
from posts.models import Post

def fitness_items(request):
    fitness = Fitness.objects.all()
    return render(request, 'fitness/fitness_items.html', {'fitness': fitness})

def lesson_page(request, param):
    posts = Post.objects.all()
    lessons = Lesson.objects.all()
    courses = Course.objects.all()
    lesson = get_object_or_404(Lesson, slug=param)
    context = {
        'posts': posts,
        'lessons': lessons,
        'courses': courses,
        'lesson': lesson
    }
    return render(request, 'fitness/lesson_page.html', context)

def course_page(request, param):
    posts = Post.objects.all()
    courses = Course.objects.all()
    lessons = Lesson.objects.all()
    course = get_object_or_404(Course, slug=param)
    context = {
        'posts': posts,
        'courses': courses,
        'lessons': lessons,
        'course': course
    }
    return render(request, 'fitness/course_page.html', context)
