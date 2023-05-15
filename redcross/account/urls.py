from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signupPage, name='user_signup'),
    path('complete-profile/', views.completeProfile, name='completeProfile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),



    # Customizing Built-in reset password
    # This path is para makuha yung email ng user
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),

    # to handle the password reset form submission
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # to handle the password reset confirmation
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # to handle the password reset complete
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
