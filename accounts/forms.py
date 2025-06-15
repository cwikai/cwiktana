from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    business_name = forms.CharField(max_length=255, required=False)
    business_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'business_name', 'business_address', 'phone_number', 'password1', 'password2']
