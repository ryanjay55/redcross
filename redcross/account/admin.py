from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import DonorInfo


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    
class CustomDonorInfoAdmin(admin.ModelAdmin):
    list_display = ('info_id', 'firstname', 'lastname', 'blood_type', 'date_of_birth', 'email', 'address', 'sex', 'occupation','age','contact_number','completed_at','is_privacy_accepted_terms_accepted','is_consent_accepted')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(DonorInfo,CustomDonorInfoAdmin)

