from django import forms
from .models import Grading  # ✅ Make sure this is the correct import

class GradingForm(forms.ModelForm):
    class Meta:
        model = Grading  # ✅ Not lowercase!
        fields = ['class_name', 'instructor', 'examiner', 'start_time', 'end_time', 'location', 'status']
