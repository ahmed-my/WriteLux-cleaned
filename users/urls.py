from django.urls import path
from .views import (
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView, CustomPasswordResetDoneView,
    register, login_user, logout_user, resend_password_reset_email,
    portfolio_view, profile_portfolio, upload_image, user_profile,
    UserListView, user_profile_list, profile_detail, edit_profile,
    inbox, message_detail, delete_message, reply_message,
    bulk_delete_messages, chat_message, send_message_form, send_message_ajax,
    delete_chat, folder_detail_view, add_folder, rename_folder, delete_folders, delete_image_view
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('registration/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),

    # Portfolio URLs
    path('portfolio/upload/', upload_image, name='upload_image'),
    path('portfolio/add-folder/', add_folder, name='add_folder'),
    path('portfolio/rename-folder/', rename_folder, name='rename_folder'),
    path('portfolio/delete-folders/', delete_folders, name='delete_folders'),
    
    #path('portfolio/<uuid:profile_id>/folder/<str:folder_name>/<int:folder_id>/delete-image/<int:image_id>/', delete_image, name='delete_image'),

    # Specific folder view by profile_id and folder_id
    # urls.py
    #path('portfolio/<uuid:profile_id>/<slug:folder_name>/<int:folder_id>/', folder_detail_view, name='folder_detail'),
    path('portfolio/<uuid:profile_id>/<str:folder_name>/<int:folder_id>/', folder_detail_view, name='folder_detail'),
    path('portfolio/<uuid:profile_id>/<int:folder_id>/<int:image_id>/delete/', delete_image_view, name='delete_image'),
    #path('portfolio/<uuid:profile_id>/folder/<int:folder_id>/', folder_detail_view, name='folder_detail'),

    # General portfolio view (least specific pattern)
    path('portfolio/', portfolio_view, name='portfolio'),

    # Profile portfolio with slug (less specific pattern)
    path('portfolio/<slug:slug>/', profile_portfolio, name='profile_portfolio'),


    # User Profile
    path('profile/', user_profile, name='user_profile'),
    path('profiles/', user_profile_list, name='user_profile_list'),
    path('profiles/<uuid:profile_id>/', profile_detail, name='profile_detail'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # Password Reset
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/resend/', resend_password_reset_email, name='resend_password_reset_email'),

    # Messaging
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<uuid:profile_id>/', profile_detail, name='profile_detail'),
    path('chat/', chat_message, name='chat_message'),
    path('send-message-ajax/', send_message_ajax, name='send_message_ajax'),
    path('delete_chat/', delete_chat, name='delete_chat'),
    path('chat/<int:user_id>/', chat_message, name='chat_message'),
    path('send_message_form/', send_message_form, name='send_message_form'),
    path('inbox/', inbox, name='inbox'),
    path('message/<int:pk>/', message_detail, name='message_detail'),
    path('message/<int:pk>/delete/', delete_message, name='delete_message'),
    path('message/<int:pk>/reply/', reply_message, name='reply_message'),
    path('bulk-delete/', bulk_delete_messages, name='bulk_delete_messages'),
]
