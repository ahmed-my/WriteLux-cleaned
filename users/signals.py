# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import send_registration_confirmation_email  # Assuming you placed it in utils.py
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

def send_confirmation_email_on_creation(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_registration_confirmation_email(instance)
