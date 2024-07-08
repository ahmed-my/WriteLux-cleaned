from django.shortcuts import render, redirect

# 5-07-24
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
# added above delete task

from .models import Post
from fitness.models import Lesson, Course
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
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
            return redirect('posts:list')
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
        return redirect_to_login(self.request.get_full_path())
# done and ok