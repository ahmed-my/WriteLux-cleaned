# users/forms.py
from django import forms
from .models import Portfolio, UserProfile, Message, Folder # 02-08-2024
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .email_utils import send_registration_confirmation_email

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='',
        widget=forms.EmailInput(attrs={
            'class': 'custom-class',
            'placeholder': 'Email Address'  # Set placeholder
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'Username'  # Set placeholder
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'Password'  # Set placeholder
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'custom-class',
            'placeholder': 'Password Confirmation'  # Set placeholder
        })
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            print("User saved, sending email...")
            send_registration_confirmation_email(user)  # Send the confirmation email
            print("Email function called.")
        return user

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={
            'required': 'Please enter your username.',
            'invalid': 'Invalid username format.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={
            'required': 'Please enter your password.',
            'invalid': 'Invalid password format.',
        }
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                'This account is inactive.',
                code='inactive',
            )

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    bio = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'profile_image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            # Access the bio from the related UserProfile instance
            self.fields['bio'].initial = user.userprofile.bio

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("Email address already in use.")
        return email

    def save(self, commit=True):
        user = self.instance.user  # Access the related User instance
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            user_profile = super(UserProfileForm, self).save(commit=False)  # Save the UserProfile instance without committing to the database yet
            user_profile.bio = self.cleaned_data['bio']  # Assuming `bio` is part of the UserProfile model
            user_profile.save()
        
        return self.instance
    
# 02-08-2024
class MessageForm(forms.ModelForm):
    recipient_id = forms.IntegerField(widget=forms.HiddenInput)  # Hidden input for recipient_id

    class Meta:
        model = Message
        fields = ['subject', 'body', 'recipient_id']  # Add recipient_id to the fields
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ReplyMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']  # Exclude recipient for replies

class PortfolioForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.none(), required=False, label="Select Folder") # 9-08-2024

    class Meta:
        model = Portfolio
        fields = ['image', 'description', 'folder']

    def __init__(self, *args, **kwargs): # 09-08-2024
        user = kwargs.pop('user', None)
        super(PortfolioForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)
