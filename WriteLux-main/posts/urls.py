from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    #path("", views.posts_list, name='list'),
    #path("new_post/", views.new_post, name='new_post'),
    #path('<slug:param>', views.post_page, name='post_page'),
    #path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'), # added delete task

    path('', views.posts_list, name='posts_list'),
    path('search/', views.search, name='search'),  # Add this line
    path('dashboard/', views.post_list, name='post_list'),
    path("new_post/", views.new_post, name='new_post'),
    path('create/', views.post_create, name='post_create'),
    path('<slug:param>/', views.post_page, name='post_page'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
]
