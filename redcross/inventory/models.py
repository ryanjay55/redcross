from django.db import models
from django.core.exceptions import ValidationError
from account.models import DonorInfo
from django.utils import timezone
from datetime import timedelta

class BloodBags(models.Model):
    bag_id = models.AutoField(primary_key=True)
    info_id = models.ForeignKey(DonorInfo, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=100, unique=True)
    date_donated = models.DateTimeField()
    bled_by = models.CharField(max_length=50)
    
    @property
    def days_since_donation(self):
        days = (timezone.now() - self.date_donated).days
        return days
    
    def get_exp_date(self):
        return self.date_donated + timedelta(days=37) # expiration date is 37 days after donation
    
    


class BloodInventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    bag_id = models.ForeignKey(BloodBags, on_delete=models.CASCADE)
    exp_date = models.DateTimeField()
    qty = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if BloodInventory.objects.filter(bag_id=self.bag_id).exists():
            raise ValidationError("Blood bag with this serial number already exists in the inventory.")

    def save(self, *args, **kwargs):
        if not self.exp_date:
            self.exp_date = self.bag_id.get_exp_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.inventory_id)
