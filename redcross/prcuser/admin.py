from django.contrib import admin
from .models import PrcUser

# Register your models here.
class PrcUserAdmin(admin.ModelAdmin):
    list_display = ['id','firstname', 'lastname', 'blood_type', 'email', 'address','age','sex','occupation','contact_number']
    search_fields= ['id','firstname', 'lastname', 'blood_type', 'email', 'address','occupation','contact_number']
    list_per_page= 25
    
admin.site.register(PrcUser,PrcUserAdmin)