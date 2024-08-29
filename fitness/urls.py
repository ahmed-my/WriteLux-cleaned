from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.fitness_home, name='fitness_home'),
    path('search/', views.search, name='search'),  # Add this line
    path('lesson/<slug:param>/', views.lesson_page, name='lesson_page'),
    path('course/<slug:param>/', views.course_page, name='course_page'),

    # Add more paths as needed, e.g., for article detail pages
    path('article/<int:id>/', views.article_detail, name='article_detail'),
]
