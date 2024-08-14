from django.shortcuts import render, get_object_or_404, redirect
from fitness.models import Image
from posts.models import Post
from fitness.models import Lesson, Course, Fitness, Home
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from posts.forms import CustomForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

def swiper_example(request):
    return render(request, 'swiper_example.html')

def home(request):
    courses = Course.objects.all()
    posts = Post.objects.all()
    lessons = Lesson.objects.all()
    home_content = Home.objects.all()
    context = {
        'courses': courses,
        'posts': posts,
        'lessons': lessons,
        'home_content': home_content
    }
    return render(request, 'home.html', context)

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
    return render(request, 'search_results.html', context)

@login_required(login_url="/users/login/")
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    courses = Course.objects.all()  # Include courses here
    context = {
        'user': user,
        'posts': posts,
        'courses': courses, # Add courses to the context
    }
    return render(request, 'dashboard.html', context)

def image_list(request):
    posts = Post.objects.all()
    courses = Course.objects.all()
    lessons = Lesson.objects.all()
    images = Image.objects.all()
    context = {
        'images': images,
        'posts': posts,
        'courses': courses,
        'lessons': lessons,
    }
    return render(request, 'image_list.html', context)

def portfolio_list(request):
    return render(request, 'portfolio_list.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(UpdateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'successfully updated!')
        return super().form_valid(form)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def generate_portfolio_url(request):
    return render(request, 'generate_url.html')

def faq(request):
    return render(request, 'faq.html')