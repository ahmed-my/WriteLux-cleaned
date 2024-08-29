# adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import User
import random
import string

class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(request, user, form, commit=False)
        user.username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        user.save()
        return user
