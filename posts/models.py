from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.text import slugify
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
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = HTMLField()
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body = bleach.clean(self.body, tags=allowed_tags, attributes=allowed_attrs)
        
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Post.objects.filter(slug__iexact=self.slug).exclude(pk=self.pk)
            counter = 1
            while queryset.exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
                queryset = Post.objects.filter(slug__iexact=self.slug).exclude(pk=self.pk)

        super(Post, self).save(*args, **kwargs)

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
