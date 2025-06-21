from django import forms
from .models import Grading

class GradingForm(forms.ModelForm):
    class Meta:
        model = Grading
        fields = '__all__'  # or list the fields you want to include
