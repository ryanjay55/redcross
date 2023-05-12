from django.db import models
from account.models import DonorInfo



class Deferral(models.Model):
    deferral_id = models.AutoField(primary_key=True)
    info_id = models.ForeignKey(DonorInfo, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    other_reason = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=20)