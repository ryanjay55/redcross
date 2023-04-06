from django.urls import path
from account import views

urlpatterns = [
  path('login/', views.loginPage, name='user_login'),
  path('logout/', views.user_logout, name='user_logout'),
  path('signup/', views.signupPage, name='user_signup'),
  path('complete-profile/', views.completeProfile, name='completeProfile'),
]