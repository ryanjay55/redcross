from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import DonorInfo
from datetime import date

# A custom widget to apply styling to password fields
class CustomPasswordInput(forms.PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'width: 100%'})



class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = DonorInfo
        fields = ['firstname', 'lastname', 'blood_type', 'date_of_birth', 'email', 'address', 'sex', 'occupation', 'contact_number', 'is_privacy_accepted_terms_accepted', 'is_consent_accepted']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firstname', 'style': 'width: 100%'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lastname', 'style': 'width: 100%'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address', 'style': 'width: 100%'}),
            # 'sex': forms.TextInput(attrs={'class': 'form-control','style': 'width: 100%'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'occupation', 'style': 'width: 100%'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control','style': 'width: 100%','type': 'date'})
            
        }
        required = {
            'occupation': False,
        }


       

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        # Perform any validation or cleaning for the contact_number field
        # For example, you can strip out any non-numeric characters, or ensure it's in a certain format
        return contact_number

    def clean_date_of_birth(self):
        """
        Validate that the date of birth is at least 17 years ago and not in the future,
        and not more than 100 years ago.
        """
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 17:
                raise forms.ValidationError("You must be at least 17 years old and above.")
            if date_of_birth > today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
            if date_of_birth.year < (today.year - 100):
                raise forms.ValidationError("Please enter a valid date of birth.")
        return date_of_birth


