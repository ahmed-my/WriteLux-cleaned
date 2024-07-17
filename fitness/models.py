from django.db import models
from tinymce.models import HTMLField
import bleach


# Update allowed tags and attributes
allowed_tags = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 
    'strong', 'bold', 'ul', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'span'
]
allowed_attrs = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'width', 'height'],
    'span': ['style']
}

# Create your models here.
class Fitness(models.Model):
    name = models.CharField(max_length=75)
    address = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # add this for the image below
    banner = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=75)
    image = models.ImageField(upload_to='images/')
    # add this for the image below
    banner = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    name = models.CharField(max_length=75)
    body = HTMLField()
    slug = models.SlugField()
    # add this for the image below
    banner = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.name
    
# 07-07-24
# create table model course
class Course(models.Model):
    title = models.CharField(max_length=75)
    body = HTMLField()
    slug = models.SlugField()
    banner = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.title
