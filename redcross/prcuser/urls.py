from django.urls import path
from prcuser import views

urlpatterns = [
  path('', views.index, name='index'),
]