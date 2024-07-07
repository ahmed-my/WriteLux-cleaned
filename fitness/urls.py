from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.fitness_items, name='fitness_items'),
    path('<slug:param>', views.lesson_page, name='lesson_page'),
    path('<slug:param>', views.course_page, name='course_page'),
]
