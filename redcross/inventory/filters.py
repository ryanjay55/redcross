import django_filters
from .models import BloodInventory

class BloodInventoryFilter(django_filters.FilterSet):
    blood_type = django_filters.CharFilter(field_name='bag_id__info_id__blood_type', lookup_expr='exact')

    class Meta:
        model = BloodInventory
        fields = ['blood_type']
