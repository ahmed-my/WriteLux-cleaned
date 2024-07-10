from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='', label='Email Address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-class'}),
            'email': forms.EmailInput(attrs={'class': 'custom-class'}),
            'password1': forms.PasswordInput(attrs={'class': 'custom-class', 'help_text': ''}),
            'password2': forms.PasswordInput(attrs={'class': 'custom-class', 'help_text': ''}),
        }
        help_texts = {
            'username': None,  # Remove help text for username
            'password1': None,  # Remove help text for password1
            'password2': None,  # Remove help text for password2
        }
        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'invalid': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
            },
            'password1': {
                'required': 'Please enter a password.',
            },
            'password2': {
                'required': 'Please confirm your password.',
            },
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'custom-class'})
        self.fields['email'].widget.attrs.update({'class': 'custom-class'})
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
