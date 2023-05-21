from django.contrib import admin
from .models import BloodBags, BloodInventory,ExpiredBlood


@admin.register(BloodBags)
class BloodBagsAdmin(admin.ModelAdmin):
    list_display = ('bag_id', 'info_id', 'serial_no', 'date_donated', 'bled_by')
    list_filter = ('date_donated',)
    search_fields = ('serial_no', 'info_id__firstname', 'info_id__lastname', 'bled_by__username')

    def info_id(self, obj):
        return f"{obj.info_id.firstname} {obj.info_id.lastname}"
    info_id.short_description = 'Donor'


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'bag_id', 'get_donor_name', 'get_serial_no', 'get_date_donated', 'exp_date')
    list_filter = ('exp_date',)
    search_fields = ('bag_id__serial_no', 'bag_id__info_id__firstname', 'bag_id__info_id__lastname')

    def get_donor_name(self, obj):
        return f"{obj.bag_id.info_id.firstname} {obj.bag_id.info_id.lastname}"
    get_donor_name.short_description = 'Donor Name'

    def get_serial_no(self, obj):
        return obj.bag_id.serial_no
    get_serial_no.short_description = 'Bag Serial No.'

    def get_date_donated(self, obj):
        return obj.bag_id.date_donated
    get_date_donated.short_description = 'Date Donated'


@admin.register(ExpiredBlood)
class ExpiredBloodAdmin(admin.ModelAdmin):
    list_display = ('bag_id', 'exp_date')
    search_fields = ('bag_id__serial_no', 'bag_id__info_id__firstname', 'bag_id__info_id__lastname')