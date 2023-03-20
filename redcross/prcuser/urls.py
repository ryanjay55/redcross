from django.urls import path
from prcuser import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('home', views.home, name='home'),
  path('signup', views.signup, name='signup'),
  
]