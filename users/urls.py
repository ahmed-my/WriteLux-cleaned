from django.urls import path
from . import views
from .views import (
    register, login_user, logout_user,
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView, CustomPasswordResetDoneView,
    resend_password_reset_email
)

app_name = 'users'

urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/upload/', views.upload_image, name='upload_image'),
    path('portfolio/<uuid:profile_id>/', views.profile_portfolio, name='profile_portfolio'),

    # Custom Password reset URLs
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Resend password reset email URL
    path('password_reset/resend/', resend_password_reset_email, name='resend_password_reset_email'),
]
