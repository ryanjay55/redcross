from django.urls import  path
from custom_admin import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users-list/', views.usersList, name='users-list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donors/', views.donors, name='donors'),
    path('mbd-summary/', views.mbdSummary, name='mbdSummary'),
    path('deferred-donors/', views.deferredDonors, name='deferredDonors'),
    # path('add_bloodbag/', views.add_bloodbag, name='add_bloodbag'),
    # path('add_blood_bag/', views.add_blood_bag, name='add_blood_bag'),
    

    
    #others
    path('export-donor-info/', views.export_donors_info, name='export-donor-info'),

]
