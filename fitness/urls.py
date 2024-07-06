from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_items, name='fitness_items'),
]
