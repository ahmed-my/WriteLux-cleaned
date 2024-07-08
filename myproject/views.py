# from django.http import HttpResponse "This is used when requesting response from http request"
from django.shortcuts import render, get_object_or_404, redirect
from fitness.models import Image
from posts.models import Post
from fitness.models import Lesson, Course
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from posts.forms import CustomForm  # Assuming you have a form for the Post model
from django.views.generic.detail import DetailView


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

# use decorator to grant access to only logged in users
@login_required(login_url="/users/login/")
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'dashboard.html', context)

def image_list(request):
    images = Image.objects.all()
    return render(request, 'image_list.html', {'images': images})

def image_logo(request):
    logo = Image.objects.all()[0]
    return render(request, 'layout.html', {'logo': logo})

def contact(request):
    post_contact = Post.objects.all()
    return render(request, 'contact.html', {'post_contact': post_contact})

class PostCreateView(CreateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/new_post.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

class PostUpdateView(UpdateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
