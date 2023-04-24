from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, date
from django.contrib.auth.models import User
import uuid



def generate_id():
    now = datetime.now()
    year = now.strftime("%y")
    unique_part = str(uuid.uuid4().fields[-1])[:4]  # Take the last 4 digits of the UUID
    return f"{year}-{unique_part}"

# Create your models here.
class DonorInfo(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    BLOOD_TYPES = (
        ('A+', 'A positive'),
        ('A-', 'A negative'),
        ('B+', 'B positive'),
        ('B-', 'B negative'),
        ('AB+', 'AB positive'),
        ('AB-', 'AB negative'),
        ('O+', 'O positive'),
        ('O-', 'O negative'),
    )
    info_id = models.CharField(max_length=7, unique=True, primary_key=True, editable=False, default=generate_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0, editable=False)
    contact_number = PhoneNumberField(default='+639')
    completed_at=models.DateTimeField(auto_now_add=True)
    is_privacy_accepted_terms_accepted = models.BooleanField(default=False)
    is_consent_accepted = models.BooleanField(default=False)
  
    def __str__(self):
        return self.firstname
    
    def calculate_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    calculate_age.short_description = 'Age'
    
    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(DonorInfo, self).save(*args, **kwargs)

    