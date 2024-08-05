# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse # to implement chat 04-08-2024
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin # to exclude a user on the lists of users
from .models import UserProfile, Portfolio, Message, Conversation # message added 02-08-2024
from .forms import UserCreationForm, UserProfileForm, UserRegistrationForm, AuthenticationForm, UserAuthenticationForm, MessageForm, ReplyMessageForm, PortfolioForm # MessageForm added 02-08-2024

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
                    
                    # Generate the full password reset link
                    reset_link = f"{context['protocol']}://{context['domain']}{reverse('users:password_reset_confirm', kwargs={'uidb64': context['uid'], 'token': context['token']})}"
                    
                    # Print the reset link to the console
                    print("Password reset link:", reset_link)
                    
                    # Send the email
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
            print("Password reset token:", token)  # Print the token to the console
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login_user')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = UserAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')

@login_required
def portfolio_view(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {'portfolio': portfolio}
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

class UserListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        # Exclude the logged-in user from the queryset
        return UserProfile.objects.exclude(user=self.request.user)

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
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile, user=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.') # display a successful update
            return redirect('dashboard')
    else:
        profile_form = UserProfileForm(instance=user.userprofile, user=user)

    return render(request, 'users/edit_profile.html', {
        'profile_form': profile_form,
        'user': user,
    })

@login_required
def chat_message(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    messages = conversation.messages.all()

    return render(request, 'users/chat_message.html', {'conversation': conversation, 'messages': messages, 'other_user': other_user})

@login_required
def send_message_form(request):
    users = UserProfile.objects.exclude(user=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient_id = request.POST.get('recipient')
            if not recipient_id:
                messages.error(request, 'Recipient is required.')
                return render(request, 'users/send_message_form.html', {'form': form, 'users': users})
            
            recipient = get_object_or_404(User, id=recipient_id)

            # Check for existing conversation
            conversation = Conversation.objects.filter(
                Q(participants=request.user) & Q(participants=recipient)
            ).distinct().first()

            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, recipient)

            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.conversation = conversation
            message.save()

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('users:inbox')
    else:
        form = MessageForm()
    
    return render(request, 'users/send_message_form.html', {'form': form, 'users': users})

@login_required
def send_message_ajax(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        text = request.POST.get('text')

        conversation = get_object_or_404(Conversation, id=conversation_id)
        recipient = conversation.participants.exclude(id=request.user.id).first()
        message = Message.objects.create(conversation=conversation, sender=request.user, recipient=recipient, body=text)

        return JsonResponse({'status': 'ok', 'message': {
            'id': message.id,
            'sender': message.sender.username,
            'body': message.body,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'users/inbox.html', {'messages': messages})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    if not message.read:
        message.read = True
        message.save()
    return render(request, 'users/message_detail.html', {'message': message})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    if request.method == 'POST':
        message.delete()
        return redirect('users:inbox')
    return render(request, 'users/delete_message_confirm.html', {'message': message})

# 03-08-2024 the reply view
@login_required
def reply_message(request, pk):
    original_message = get_object_or_404(Message, pk=pk, recipient=request.user)
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = original_message.sender
            reply.save()
            # messages.success(request, 'reply sent.') need to fix this to work properly
            return redirect('users:inbox')
        else:
            print(form.errors)  # Add this line to print form errors to the console
    else:
        form = ReplyMessageForm(initial={'subject': 'Re: ' + original_message.subject})

    return render(request, 'users/reply_message.html', {'original_message': original_message, 'form': form})

def bulk_delete_messages(request):
    if request.method == 'POST':
        selected_messages = request.POST.getlist('selected_messages')
        if selected_messages:
            Message.objects.filter(pk__in=selected_messages).delete()
            messages.success(request, 'Selected messages have been deleted.')
        else:
            messages.warning(request, 'No messages were selected.')
    return redirect('users:inbox')
