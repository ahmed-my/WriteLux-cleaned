from django import forms
from . import models

class CustomForm(forms.ModelForm):
    
    class Meta:
        model = models.Post
        fields = ("title", "body", "slug", "banner")
