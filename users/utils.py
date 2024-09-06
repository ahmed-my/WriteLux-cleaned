# users/utils.py
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

def generate_confirmation_token(user):
    return default_token_generator.make_token(user)

def send_registration_confirmation_email(user, token):
    # Encode user ID to uidb64 format
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Generate dynamic confirmation URL
    confirmation_url = settings.SITE_URL + reverse('users:email_confirm', kwargs={'uidb64': uidb64, 'token': token})

    subject = 'Confirm your registration'
    message = f'Hi {user.username},\n\nPlease click the link below to confirm your registration:\n\n{confirmation_url}'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
