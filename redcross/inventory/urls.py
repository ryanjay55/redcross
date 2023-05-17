from django.urls import  path
from inventory import views

urlpatterns = [
    # path('bloodBagList/', views.bloodBagList, name='bloodBagList'),
    path('blood-inventory-overview/', views.bloodInventory, name='bloodInventory'),
    path('blood-bag-list/', views.bloodBagList, name='bloodBagList'),
    
    
    #others
    path('exportBloodBagList_to_xls/', views.exportBloodBagList_to_xls, name='exportBloodBagList_to_xls'),
]