from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            num = 1
            while UserProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

# creating folders for portfolio images 09-08-2024
class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure uniqueness
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    folder = models.ManyToManyField(Folder, related_name='portfolio_images', blank=True)  # Changed to ManyToManyField
    # folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='portfolio_images', null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.user.username}'s portfolio image"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    subject = models.CharField(max_length=255, blank=True, null=True)

class Message(models.Model):
    subject = models.CharField(blank=True, max_length=100, null=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey('Conversation', related_name='messages', on_delete=models.CASCADE)  # remove default value here
    is_chat = models.BooleanField(default=False)  # New field to indicate chat messages

    def __str__(self):
        return f'From {self.sender} to {self.recipient}'

# Model for Contact Query    
class ContactQuery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"