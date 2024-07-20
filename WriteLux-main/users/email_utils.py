# users/email_utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_registration_confirmation_email(user):
    print("Preparing to send email...")
    subject = 'Welcome to Your Site'
    html_message = render_to_string('users/registration_confirmation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    print("Email sent to:", user.email)
