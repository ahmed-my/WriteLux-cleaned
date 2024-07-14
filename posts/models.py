from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import bleach

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'bold', 'ul', 'p', 'h1', 'h2']
allowed_attrs = {'a': ['href', 'title']}

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=75)
    body = HTMLField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    # add this for the image below
    banner = models.ImageField(default='fallback.png', blank=True)
    # to know a specific user who added a post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Clean the body content using bleach before saving
        self.body = bleach.clean(self.body, tags=allowed_tags, attributes=allowed_attrs)
        super(Post, self).save(*args, **kwargs)

# 07-07-24
# create table model course
class Course(models.Model):
    title = models.CharField(max_length=75)
    body = HTMLField()
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Clean the body content using bleach before saving
        self.body = bleach.clean(self.body, tags=allowed_tags, attributes=allowed_attrs)
        super(Course, self).save(*args, **kwargs)
