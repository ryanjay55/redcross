from django.urls import  path
from inventory import views

urlpatterns = [
    path('bloodBagList/', views.bloodBagList, name='bloodBagList'),
    path('bloodInventory/', views.bloodInventory, name='bloodInventory'),
    
    
    #others
    path('exportBloodBagList_to_xls/', views.exportBloodBagList_to_xls, name='exportBloodBagList_to_xls'),
]