from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, date



# Create your models here.
class PrcUser(models.Model):
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
    
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    date_of_birth = models.DateField(null=True, blank=True)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    contact_number = PhoneNumberField(default='+639')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.firstname
    
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    age.short_description = 'Age'
    
    