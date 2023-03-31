from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# A custom widget to apply styling to password fields
class CustomPasswordInput(forms.PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'width: 100%'})

# A custom form that extends UserCreationForm to add styling to fields
class CreateUserForm(UserCreationForm):
    # Apply the custom widget to password fields
    password1 = forms.CharField(widget=CustomPasswordInput)
    password2 = forms.CharField(widget=CustomPasswordInput)

    class Meta:
        # Set the model and fields to be used in the form
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Apply styling to the username and email fields
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'style': 'width: 100%'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'style': 'width: 100%'}),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Add password validation criteria here
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username
