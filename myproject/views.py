# from django.http import HttpResponse "This is used when requesting response from http request"
from django.shortcuts import render
from fitness.models import Image
from posts.models import Post
from fitness.models import Lesson, Course
from django.contrib.auth.decorators import login_required

def home(request):
    # return HttpResponse("Hello World!. You are home")
    courses = Course.objects.all() # Fetch all courses
    posts = Post.objects.all()  # Fetch all posts
    lessons = Lesson.objects.all() # Fetch all lessons
    context = {
        'courses': courses,
        'posts': posts,
        'lessons': lessons
    }
    return render(request, 'home.html', context)
    
def about(request):
    # return HttpResponse("The about page")
    return render(request, 'about.html')

# use decorator to grant access to only logged in users
@login_required(login_url="/users/login/")
def image_list(request):
    images = Image.objects.all()
    return render(request, 'image_list.html', {'images': images})

def image_logo(request):
    logo = Image.objects.all()[0]
    return render(request, 'layout.html', {'logo': logo})

def contact(request):
    post_contact = Post.objects.all()
    return render(request, 'contact.html', {'post_contact': post_contact})