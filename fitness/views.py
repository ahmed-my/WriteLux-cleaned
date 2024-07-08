from django.shortcuts import render, get_object_or_404
from .models import Fitness, Image, Lesson, Course
from posts.models import Post

def fitness_items(request):
    fitness = Fitness.objects.all()
    return render(request, 'fitness/fitness_items.html', {'fitness': fitness})

def search(request):
    query = request.GET.get('q')
    if query:
        fitness_results = Fitness.objects.filter(name__icontains=query)
        lesson_results = Lesson.objects.filter(name__icontains=query)
        course_results = Course.objects.filter(title__icontains=query)
        post_results = Post.objects.filter(title__icontains=query)
    else:
        fitness_results = Fitness.objects.none()
        lesson_results = Lesson.objects.none()
        course_results = Course.objects.none()
        post_results = Post.objects.none()

    context = {
        'query': query,
        'fitness': fitness_results,
        'lessons': lesson_results,
        'courses': course_results,
        'posts': post_results
    }
    return render(request, 'fitness/search_results.html', context)

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
