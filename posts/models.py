from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    # add this for the image below
    banner = models.ImageField(default='fallback.png', blank=True)
    # to know a specific user who added a post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
    
# 07-07-24
# create table model course
class Course(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.title
