from django.contrib import admin
from .models import BloodBags

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