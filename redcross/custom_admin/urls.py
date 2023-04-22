from django.urls import  path
from custom_admin import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('export-donor-info/', views.export_donors_info, name='export-donor-info'),
]
