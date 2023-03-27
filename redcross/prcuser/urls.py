from django.urls import path
from prcuser import views

urlpatterns = [
  path('', views.index, name='index'),
  path('loginPage', views.loginPage, name='loginPage'),
  path('home', views.home, name='home'),
  path('signup', views.signup, name='signup'),
  path('dashboard', views.dashboard, name='dashboard'),
  
]