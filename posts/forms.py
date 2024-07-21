from django import forms
from tinymce.widgets import TinyMCE
from . import models

class CustomForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    
    class Meta:
        model = models.Post
        fields = ("title", "body", "slug", "banner")  # Adjust fields as needed

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if models.Post.objects.filter(title=title, author=self.author).exists():
            raise forms.ValidationError("A post with this title already exists.")
        return title
