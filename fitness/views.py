from django.shortcuts import render, get_object_or_404
from .models import Fitness, Image, Lesson, Course, Home, Article, Tip, Quote
from posts.models import Post

def fitness_home(request):
    fitness = Fitness.objects.all()
    articles = Article.objects.all().order_by('-published_date')
    tips = Tip.objects.all().order_by('order')
    quotes = Quote.objects.all()

    context = {
        'fitness': fitness,
        'articles': articles,
        'tips': tips,
        'quotes': quotes,
    }
    return render(request, 'fitness/fitness_home.html', context)

# New article_detail view
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    context = {
        'article': article,
    }
    return render(request, 'fitness/article_detail.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        fitness_results = Fitness.objects.filter(name__icontains=query)
        article_results = Article.objects.filter(title__icontains=query)
        tip_results = Tip.objects.filter(title__icontains=query)
        quote_results = Quote.objects.filter(content__icontains=query)
    else:
        fitness_results = Fitness.objects.none()
        article_results = Article.objects.filter()
        tip_results = Tip.objects.filter()
        quote_results = Quote.objects.filter()

    context = {
        'query': query,
        'fitness': fitness_results,
        'articles': article_results,
        'tips': tip_results,
        'Quotes': quote_results,
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
