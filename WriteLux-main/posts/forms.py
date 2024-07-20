from django import forms
from tinymce.widgets import TinyMCE
from . import models

class CustomForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = models.Post
        fields = ("title", "body", "slug", "banner") # Adjust fields as needed
