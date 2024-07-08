from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.fitness_items, name='fitness_items'),
    path('search/', views.search, name='search'),  # Add this line
    path('lesson/<slug:param>/', views.lesson_page, name='lesson_page'),
    path('course/<slug:param>/', views.course_page, name='course_page'),
]
