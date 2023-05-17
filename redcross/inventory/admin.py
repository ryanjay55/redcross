from django.contrib import admin
from .models import BloodBags,BloodInventory

@admin.register(BloodBags)
class BloodBagsAdmin(admin.ModelAdmin):
    list_display = ('bag_id', 'info_id_id', 'info_id_first_name', 'info_id_last_name', 'serial_no', 'date_donated', 'bled_by')
    list_filter = ('date_donated',)
    search_fields = ('serial_no', 'info_id__first_name', 'info_id__last_name', 'bled_by')

    def info_id_first_name(self, obj):
        return obj.info_id.firstname
    info_id_first_name.short_description = 'Donor First Name'

    def info_id_last_name(self, obj):
        return obj.info_id.lastname
    info_id_last_name.short_description = 'Donor Last Name'
    
    
    
@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'get_info_id', 'get_name', 'get_serial_no', 'get_date_donated', 'exp_date', 'qty')
    list_filter = ('exp_date',)
    search_fields = ('bag_id__serial_no', 'bag_id__info_id__firstname', 'bag_id__info_id__lastname')
    
    def get_info_id(self, obj):
        return obj.bag_id.info_id_id
    get_info_id.short_description = 'Donor ID'
    
    def get_name(self, obj):
        return f"{obj.bag_id.info_id.firstname} {obj.bag_id.info_id.lastname}"
    get_name.short_description = 'Donor Name'
    
    def get_serial_no(self, obj):
        return obj.bag_id.serial_no
    get_serial_no.short_description = 'Bag Serial No.'
    
    def get_date_donated(self, obj):
        return obj.bag_id.date_donated
    get_date_donated.short_description = 'Date Donated'
