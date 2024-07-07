from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.posts_list, name='list'),
    path("new_post/", views.new_post, name='new_post'),
    path('<slug:param>', views.post_page, name='post_page'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'), # added delete task
]
