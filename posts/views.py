from django.shortcuts import render, get_object_or_404, redirect

# 5-07-24
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.contrib import messages
# added above delete task

from .models import Post
from fitness.models import Lesson, Course, Fitness
from django.contrib.auth.decorators import login_required
from . import forms

from .forms import CustomForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# Create your views here.

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Add your logic to handle the contact form submission (e.g., send an email, save to a model)
        messages.success(request, 'Your message has been sent!')
        return redirect(reverse('posts:contact'))
    return render(request, 'posts/contact.html')

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add your logic to handle the email signup (e.g., saving to a model)
        messages.success(request, 'Thank you for signing up!')
        return redirect(reverse('posts:newsletter_signup'))
    return render(request, 'posts/newsletter_signup.html')

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
    return render(request, 'posts/search_results.html', context)

def posts_list(request):
    # function created posts_list
    posts = Post.objects.all().order_by('-date')
    courses = Course.objects.all()
    lessons = Lesson.objects.all() # Fetch all lessons from the lesson model in the fitness app
    context = {
        'posts': posts,
        'lessons': lessons,
        'courses': courses
    }
    return render(request, 'posts/posts_list.html', context)

def post_page(request, param):
    post = Post.objects.get(slug=param)
    courses = Course.objects.all()
    lessons = Lesson.objects.all() # Fetch all lessons from the lesson model in the fitness app
    context = {
        'post': post,
        'lessons': lessons,
        'courses': courses
    }
    return render(request, 'posts/post_page.html', context) 

@login_required(login_url="/users/login/")
def new_post(request):
    if request.method == 'POST':
        form = CustomForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = request.user
            new_form.save()
            return redirect('posts:post_list')
        else:
            print(form.errors)  # Add this line to print form errors
    else:
        form = CustomForm(author=request.user)
    return render(request, 'posts/new_post.html', {'form': form})

# 05-07-24
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')  # Redirect to the list of posts after deletion
    template_name = 'posts/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect(self.request.get_full_path())
# done and ok

class PostListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'

class PostCreateView(CreateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        print(context['courses'])  # Debug statement
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Your post was successfully updated!')
        return super().form_valid(form)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

post_list = PostListView.as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()
post_detail = PostDetailView.as_view()