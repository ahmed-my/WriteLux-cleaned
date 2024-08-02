# users/urls.py
from django.urls import path
from .views import (
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView, CustomPasswordResetDoneView,
    register, login_user, logout_user, resend_password_reset_email,
    portfolio_view, profile_portfolio, upload_image, user_profile,
    UserListView, user_profile_list, profile_detail, edit_profile
)

app_name = 'users'

urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),

    path('portfolio/', portfolio_view, name='portfolio'),
    path('portfolio/upload/', upload_image, name='upload_image'),
    path('portfolio/<slug:slug>/', profile_portfolio, name='user_portfolio'),
    path('profile/', user_profile, name='user_profile'),
    path('users/', UserListView.as_view(), name='user-list'),

    path('profiles/', user_profile_list, name='user_profile_list'),
    path('profiles/<uuid:profile_id>/', profile_detail, name='profile_detail'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_reset/resend/', resend_password_reset_email, name='resend_password_reset_email'),
]
