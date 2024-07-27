from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Portfolio
from .forms import PortfolioForm
from django.views.generic import ListView, DetailView
from .models import UserProfile
from .forms import UserProfileForm

UserModel = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'registration/password_reset.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = UserModel.objects.filter(email=email)
            
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.META['HTTP_HOST'],
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email_content = render_to_string(email_template_name, context)
                    send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, "Password reset email has been sent.")
                return redirect("users:password_reset_done")
            else:
                messages.error(request, "No user is associated with this email.")
        else:
            messages.error(request, "Invalid email address.")
    else:
        password_reset_form = PasswordResetForm()
    return render(request, "registration/password_reset.html", {"password_reset_form": password_reset_form})

def password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == "POST":
            set_password_form = SetPasswordForm(user, request.POST)
            if set_password_form.is_valid():
                set_password_form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now.")
                return redirect("users:password_reset_complete")
        else:
            set_password_form = SetPasswordForm(user)
    else:
        validlink = False
        set_password_form = None

    return render(request, "registration/password_reset_confirm.html", {
        "form": set_password_form,
        "validlink": validlink,
    })

@csrf_exempt
def resend_password_reset_email(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
            send_mail(
                "Password Reset",
                f"Click the link to reset your password: {reset_url}",
                "from@example.com",
                [email],
                fail_silently=False,
            )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login_user')  # Adjust redirect as necessary
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Login 
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')

@login_required
def portfolio_view(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {
        'portfolio': portfolio
    }
    return render(request, 'portfolio/portfolio.html', context)

@login_required
def profile_portfolio(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    portfolio_images = Portfolio.objects.filter(user=profile.user)
    context = {
        'profile': profile,
        'portfolio_images': portfolio_images,
    }
    return render(request, 'users/profile_portfolio.html', context)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_image = form.save(commit=False)
            portfolio_image.user = request.user
            portfolio_image.save()
            return redirect('dashboard')
    else:
        form = PortfolioForm()
    return render(request, 'portfolio/upload_image.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    portfolio_images = Portfolio.objects.filter(user=user)
    context = {
        'user': user,
        'profile': profile,
        'portfolio_images': portfolio_images,
    }
    return render(request, 'users/user_profile.html', context)

class UserListView(ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
    slug_field = 'profile_id'
    slug_url_kwarg = 'profile_id'

def user_profile_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'users/user_profile_list.html', {'profiles': profiles})
    
def profile_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, profile_id=profile_id)
    portfolio_images = Portfolio.objects.filter(user=profile.user)
    context = {
        'profile': profile,
        'portfolio_images': portfolio_images
    }
    return render(request, 'users/profile_detail.html', context)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Update the user model
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update the user profile model
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('dashboard')  # Change this to your profile view name

    else:
        profile_form = UserProfileForm(instance=user.userprofile)

    return render(request, 'users/edit_profile.html', {
        'profile_form': profile_form,
        'user': user,
    })