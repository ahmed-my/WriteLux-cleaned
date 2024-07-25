# users/forms.py

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Portfolio # adding the Portfolio models
from .email_utils import send_registration_confirmation_email  # Import the utility function

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['image', 'description']
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text='',
        widget=forms.EmailInput(attrs={
            'class': 'custom-class',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Remove labels and add placeholders for each field
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'username'
        })
        self.fields['username'].help_text = ''

        self.fields['email'].label = ''  # Remove the label for email
        self.fields['email'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'email'
        })
        self.fields['email'].help_text = ''
        
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'Password'
        })
        self.fields['password1'].help_text = ''

        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'Confirm Password'
        })
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            print("User saved, sending email...")
            send_registration_confirmation_email(user)  # Send the confirmation email
            print("Email function called.")
        return user
