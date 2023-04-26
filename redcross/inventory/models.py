from django.db import models
from account.models import DonorInfo

# Create your models here.

class BloodBags(models.Model):
    bag_id = models.AutoField(primary_key=True)
    info_id = models.ForeignKey(DonorInfo, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=100, unique=True)
    date_donated = models.DateTimeField()
    bled_by = models.CharField(max_length=50)

