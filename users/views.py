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
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest # to implement chat 04-08-2024
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin # to exclude a user on the lists of users
from .models import UserProfile, Portfolio, Message, Conversation, User, Folder, ContactQuery # message added 02-08-2024
from django.utils import timezone # using time and day for chat
from .forms import UserCreationForm, UserProfileForm, UserRegistrationForm, AuthenticationForm, UserAuthenticationForm, MessageForm, ReplyMessageForm, PortfolioForm, Folder # MessageForm added 02-08-2024
from itertools import groupby
import uuid

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
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.META['HTTP_HOST'],
                        "site_name": "WriteLux",
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
                # No user found with the provided email, show an error message
                messages.error(request, "No user found with this email. Please enter a valid registered email")
                return render(request, "registration/password_reset.html", {"password_reset_form": password_reset_form})
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
                "my.writelux@gmail.com",
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
    folders = Folder.objects.filter(user=request.user)  # 09-08-2024
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {
        'portfolio': portfolio,
        'folders': folders
    }
    return render(request, 'portfolio/portfolio.html', context)

@login_required
def folder_detail_view(request, profile_id, folder_name, folder_id):
    # Get the user profile based on profile_id
    user_profile = get_object_or_404(UserProfile, profile_id=profile_id)

    # Retrieve the user associated with the profile
    user = user_profile.user

    # Ensure that the logged-in user is the owner of the profile
    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    # Fetch the folder using the folder_id and folder_name
    folder = get_object_or_404(Folder, id=folder_id, user=user, name=folder_name)

    # Retrieve images associated with the folder
    images = Portfolio.objects.filter(folder=folder)

    print(images)  # Debugging line

    # Debugging: Print out the details of images retrieved
    print(f"Folder: {folder.name}")
    print("Images retrieved:")
    for image in images:
        print(f"ID: {image.id}, URL: {image.image.url}, Description: {image.description}")

    # Debugging: Print out the images retrieved
    print(f"Images in folder '{folder.name}': {[image.image.url for image in images]}")

    context = {
        'profile_id': profile_id,  # Explicitly pass profile_id
        'folder': folder,
        'images': images,
        'title': folder.name,
        'profile': request.user.userprofile  # Ensure this is available in your context
    }
    return render(request, 'portfolio/folder_detail.html', context)

@login_required
def add_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        user = request.user

        # Check if a folder with the same name already exists for this user
        if Folder.objects.filter(user=user, name=folder_name).exists():
            messages.error(request, 'Folder name already exists')
            return redirect('users:add_folder')  # Redirect back to the Add Folder page

        # If the folder does not exist, create a new folder
        Folder.objects.create(user=user, name=folder_name)
        messages.success(request, 'Folder added successfully')
        return redirect('users:portfolio')  # Redirect to the portfolio page

    return render(request, 'portfolio/add_folder.html')

@login_required
def rename_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)  # Ensure the folder belongs to the logged-in user

    if request.method == "POST":
        new_name = request.POST.get('folder_name').strip()  # Get the new folder name and strip whitespace

        if new_name:
            if new_name == folder.name:
                messages.info(request, "The new name is the same as the current name. Please enter a different name.")
            elif Folder.objects.filter(name=new_name, user=request.user).exists():
                messages.info(request, "A folder with that name already exists. Please choose a different name.")
            else:
                folder.name = new_name
                folder.save()
                messages.success(request, "Folder renamed successfully")
                return redirect('users:portfolio')
        else:
            messages.info(request, "Please enter a valid folder name.")
    
    return render(request, 'portfolio/rename_folder.html', {'current_folder_name': folder.name, 'folder': folder})

@login_required # 09-08-2024 delete a folder
def delete_folders(request):
    if request.method == 'POST':
        folder_ids = request.POST.getlist('folders')
        if folder_ids:
            Folder.objects.filter(id__in=folder_ids, user=request.user).delete()
    return redirect('users:portfolio')

@login_required
def profile_portfolio(request, slug):
    print(f"Slug received: {slug}")
    profile = get_object_or_404(UserProfile, slug=slug)
    print(f"Profile found: {profile}")

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
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()

            # Handling the folder_ids from the hidden input field
            folder_ids = request.POST.get('folder_ids', '')
            if folder_ids:
                folder_ids_list = folder_ids.split(',')
                folders = Folder.objects.filter(id__in=folder_ids_list, user=request.user)
                portfolio.folder.set(folders)

            messages.success(request, "Image uploaded successfully!")
            return redirect('users:portfolio')
        else:
            messages.error(request, "Failed to upload image. Please correct the errors below.")
    else:
        form = PortfolioForm()

    folders = Folder.objects.filter(user=request.user)
    return render(request, 'users/upload_image.html', {
        'form': form,
        'selected_folders': folders,
        'folder_count': folders.count(),
    })
    
"""
@login_required
def upload_image(request):
    folder_ids = request.GET.get('folder_ids')
    selected_folders = None

    if folder_ids:
        folder_ids = folder_ids.split(',')
        selected_folders = Folder.objects.filter(id__in=folder_ids, user=request.user)

    folder_count = len(selected_folders) if selected_folders else 0

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            portfolio_image = form.save(commit=False)  # Create but don't save to DB yet
            portfolio_image.user = request.user
            portfolio_image.save()  # Save the Portfolio instance first to get a valid ID
    
            if selected_folders:
                portfolio_image.folder.set(selected_folders)  # Set the ManyToMany relationship
                portfolio_image.save()  # Save the relationship                                                                                                                                             

            # Debugging: Log the folders associated with the portfolio_image
            print(f"Folders associated with {portfolio_image}: {portfolio_image.folder.all()}")

            return redirect('users:portfolio')
    else:
        form = PortfolioForm(user=request.user)

    return render(request, 'portfolio/upload_image.html', {
        'form': form,
        'selected_folders': selected_folders,
        'folder_count': folder_count  # Pass folder count to the template
    })
"""

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
    # portfolio_images = Portfolio.objects.filter(user=profile.user)
    portfolio = Portfolio.objects.all()
    context = {
        'profile': profile,
        'portfolio': portfolio
    }
    return render(request, 'users/profile_detail.html', context)

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile  # Fetch the user's profile

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)

        # Check if the form has changed
        if profile_form.has_changed():
            if profile_form.is_valid():
                profile_form.save()
                # Since the success message is handled in JavaScript, no need to pass messages here
                return redirect('users:user_profile')  # Redirect to the user profile page
        else:
            # If the form hasn't changed, you can also optionally log or handle this
            # The "No changes made" alert is shown by the JavaScript on the front-end
            return redirect('users:user_profile')

    else:
        # Initial form rendering with the user's current information
        profile_form = UserProfileForm(instance=user_profile, user=request.user)

    context = {
        'profile_form': profile_form,
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def chat_message(request):
    user_ids = request.GET.get('users', '').split(',')
    if not user_ids:
        return redirect('users:user-list')

    try:
        user_ids = [uuid.UUID(user_id) for user_id in user_ids]
    except ValueError:
        return redirect('users:user-list')

    other_users = UserProfile.objects.filter(profile_id__in=user_ids).values_list('user', flat=True)
    if not other_users:
        return redirect('users:user-list')

    other_users = User.objects.filter(id__in=other_users)
    if not other_users.exists():
        return redirect('users:user-list')

    # Get or create a conversation involving the current user and the selected users
    conversation = Conversation.objects.filter(participants=request.user).filter(participants__in=other_users).distinct().first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        for user in other_users:
            conversation.participants.add(user)

    messages = conversation.messages.all().order_by('timestamp')

    # Group messages by day
    message_days = [
        {
            'day': date,
            'messages': list(messages_for_day)
        }
        for date, messages_for_day in groupby(messages, key=lambda x: x.timestamp.date())
    ]

    return render(request, 'users/chat_message.html', {
        'conversation': conversation,
        'message_days': message_days,
        'other_users': other_users
    })

@login_required
def send_message_form(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        print("Form data received:", request.POST)  # Debugging statement
        if form.is_valid():
            recipient_id = form.cleaned_data['recipient_id']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            print("Recipient ID:", recipient_id)
            print("Subject:", subject)
            print("Body:", body)

            if not recipient_id:
                messages.error(request, 'Recipient is required.')
                return render(request, 'users/send_message_form.html', {'form': form, 'users': users})

            recipient = get_object_or_404(User, id=recipient_id)

            # Check for existing conversation based on subject
            conversation = Conversation.objects.filter(
                Q(participants=request.user) & Q(participants=recipient) & Q(subject=subject)
            ).distinct().first()

            if not conversation:
                conversation = Conversation.objects.create(subject=subject)
                conversation.participants.add(request.user, recipient)

            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.conversation = conversation
            message.save()

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('dashboard')
        else:
            print("Form errors:", form.errors)  # Debugging statement
            messages.error(request, 'There was an error with your submission.')
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
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            body=text,
            is_chat=True  # Mark this message as a chat message
        )

        return JsonResponse({'status': 'ok', 'message': {
            'id': message.id,
            'sender': message.sender.username,
            'body': message.body,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }})

@login_required
def inbox(request):
    # Get messages that are not chat messages
    received_messages = Message.objects.filter(
        recipient=request.user
    ).exclude(is_chat=True).order_by('-timestamp')

    return render(request, 'users/inbox.html', {'received_messages': received_messages})


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


@login_required
def delete_chat(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)

        # Check if the user is the sender or recipient
        if message.sender == request.user or message.recipient == request.user:
            message.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return HttpResponseForbidden('You do not have permission to delete this message.')
    return HttpResponseForbidden('Invalid request method.')

# implement image deletion from a folder
@login_required
def delete_image_view(request, profile_id, folder_id, image_id):
    if request.method == 'POST':
        # Get the user profile
        user_profile = get_object_or_404(UserProfile, profile_id=profile_id)

        # Ensure that the logged-in user is the owner of the profile
        if request.user != user_profile.user:
            return HttpResponseForbidden("You are not allowed to delete this image.")
        
        # Retrieve the image based on image_id and folder_id
        # views.py

        image = get_object_or_404(Portfolio, id=image_id, folder__id=folder_id)
        
        # Delete the image
        image.delete()
        
        return JsonResponse({'success': True})  # Respond with JSON

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def folder_public_view(request, profile_id, folder_name, folder_id):
    user_profile = get_object_or_404(UserProfile, profile_id=profile_id)
    folder = get_object_or_404(Folder, id=folder_id, name=folder_name, user__userprofile__profile_id=profile_id)
    images = Portfolio.objects.filter(folder=folder)
    context = {
        'profile': user_profile,
        'folder': folder,
        'images': images,
        'title': f"{folder.name} Portfolio",
    }
    return render(request, 'portfolio/folder_public.html', context)

# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email
        send_mail(
            f"Contact Us: {subject}",
            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],  # Replace with your contact email from environ varaible
            fail_silently=False,
        )

        # Save query to the database
        ContactQuery.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return render(request, 'contact.html')
    
    return render(request, 'contact.html')
