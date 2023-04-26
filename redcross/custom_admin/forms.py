from django import forms
from inventory.models import BloodBags

class BloodBagForm(forms.ModelForm):
    class Meta:
        model = BloodBags
        fields = ['info_id', 'serial_no', 'date_donated', 'bled_by']
        widgets = {
            'date_donated': forms.DateInput(attrs={'type': 'date'})
        }
