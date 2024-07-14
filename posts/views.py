from django.shortcuts import render, get_object_or_404, redirect

# 5-07-24
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
# added above delete task

from .models import Post
from fitness.models import Lesson, Course, Fitness
from django.contrib.auth.decorators import login_required
from . import forms

from .forms import CustomForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# Create your views here.

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
        form = forms.CustomForm(request.POST, request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.author = request.user
            newForm.save()
            return redirect('posts:post_list')
    else:
        form = forms.CustomForm()
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

class PostUpdateView(UpdateView):
    model = Post
    form_class = CustomForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

post_list = PostListView.as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()
post_detail = PostDetailView.as_view()