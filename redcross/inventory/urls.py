from django.urls import  path
from inventory import views

urlpatterns = [
    # path('bloodBagList/', views.bloodBagList, name='bloodBagList'),
    path('blood-inventory/', views.bloodInventory, name='bloodInventory'),
    path('blood-bag-list/', views.bloodBagList, name='bloodBagList'),
    path('expiredblood/', views.expiredBlood, name='expiredBlood'),
    
    #others
    path('exportBloodBagList_to_xls/', views.exportBloodBagList_to_xls, name='exportBloodBagList_to_xls'),
]