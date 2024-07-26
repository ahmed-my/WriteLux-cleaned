# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio_images/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s portfolio image"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Other profile fields

    def __str__(self):
        return self.user.username
