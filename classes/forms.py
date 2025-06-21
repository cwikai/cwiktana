from django import forms
from .models import ClassSession

class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ['class_name', 'instructor', 'start_time', 'end_time', 'location', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
