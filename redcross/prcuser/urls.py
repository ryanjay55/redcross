from django.urls import path
from prcuser import views

urlpatterns = [
  path('', views.index, name='index'),
  path('home', views.home, name='home'),
  path('dashboard', views.dashboard, name='user-dashboard'),
  
]