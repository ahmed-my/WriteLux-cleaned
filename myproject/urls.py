"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# ahmed added below
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, dashboard


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'), 
    path('search/', views.search, name='search'),  # Add this line
    path("dashboard/", views.dashboard, name='dashboard'),
    path("image/", views.image_list, name='image'),
    path("posts/", include('posts.urls')), # Include the URLs from the postss app
    path('fitness/', include('fitness.urls')), # Include the URLs from the fitness app
    path('users/', include('users.urls')),  # Include the URLs from the users app
    path('tinymce/', include('tinymce.urls')),

    path('dashboard/post/new/', PostCreateView.as_view(), name='post_create'),
    path('dashboard/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('dashboard/post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('dashboard/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add this image path to the urlpatterns above
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)