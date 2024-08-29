from django.urls import path
from . import views
from .views import PostUpdateView, PostDetailView, PostCreateView, PostDeleteView

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
     path('contact/', views.contact, name='contact'),
    path('newsletter_signup/', views.newsletter_signup, name='newsletter_signup'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.post_list, name='post_list'),
    path('new_post/', views.new_post, name='new_post'),
    path('<slug:param>/', views.post_page, name='post_page'),
    
    # Class-based view URLs
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
