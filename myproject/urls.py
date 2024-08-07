from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, generate_profile_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'), 
    path('search/', views.search, name='search'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("image/", views.image_list, name='image'),
    path('generate-profile-url/', generate_profile_url, name='generate_profile_url'),
    
    path("posts/", include('posts.urls')),  # Include the URLs from the posts app
    path('fitness/', include('fitness.urls')),  # Include the URLs from the fitness app
    path('users/', include('users.urls')),  # Include the URLs from the users app
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('swiper_example/', views.swiper_example, name='swiper_example'),

    path('dashboard/post/new/', PostCreateView.as_view(), name='post_create'),
    path('dashboard/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('dashboard/post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('dashboard/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('accounts/', include('allauth.urls')),  # Include allauth URLs

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
