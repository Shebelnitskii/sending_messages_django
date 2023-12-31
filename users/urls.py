from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, reset_password, EmailVerificationView, \
    email_verification_failed_view, email_verified_view

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/reset_password', reset_password, name='reset_password'),
    path('verify_email/<str:token>/', EmailVerificationView.as_view(), name='verify_email'),
    path('email-verified/', email_verified_view, name='email_verified'),
    path('email-verification-failed/', email_verification_failed_view, name='email_verification_failed'),
]
