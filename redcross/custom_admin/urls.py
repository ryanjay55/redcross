from django.urls import  path
from custom_admin import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users-list/', views.usersList, name='users-list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    #others
    path('export-donor-info/', views.export_donors_info, name='export-donor-info'),

]
