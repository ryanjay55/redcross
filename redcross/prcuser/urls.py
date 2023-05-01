from django.urls import path
from prcuser import views

urlpatterns = [
  path('', views.index, name='index'),
  path('home/', views.home, name='home'),
  path('dashboard/', views.dashboard, name='user-dashboard'),
  path('blood-journey/', views.bloodJourney, name='bloodJourney'),
  path('donation-history/', views.donationHistory, name='donationHistory'),
  path('blood-donor-network/', views.bloodDonorNetowrk, name='bloodDonorNetowrk'),
  path('profile/', views.profile, name='profile'),
  
]