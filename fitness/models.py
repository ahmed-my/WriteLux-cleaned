from django.db import models

# Create your models here.
class Fitness(models.Model):
    name = models.TextField()
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
    name = models.TextField()
    body = models.TextField()
    slug = models.SlugField()
    # add this for the image below
    # banner = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.name
