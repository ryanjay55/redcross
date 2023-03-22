from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from .models import PrcUser
from datetime import timedelta, datetime



class SignupForm(forms.ModelForm):
    class Meta:
        model=PrcUser
        fields=('firstname', 'lastname', 'blood_type', 'email','date_of_birth' , 'address','sex','occupation','contact_number')
        
        
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        age = (now().date() - dob) // timedelta(days=365.25)
        if age < 17:
            raise forms.ValidationError("You must be 17 years or older to register.")
        return dob