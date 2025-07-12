from django import forms
from .models import GradingSheetTemplate
#from .models import syllabus
from .models import Belt

class GradingSheetTemplateForm(forms.ModelForm):
    class Meta:
        model = GradingSheetTemplate
        fields = ['name', 'is_active']

class BeltForm(forms.ModelForm):
    class Meta:
        model = Belt
        fields = ['grade', 'belt_colour', 'is_active']
        





#class syllabusForm(forms.ModelForm):
    #class Meta:
        #model = syllabus
        #fields = ['name', 'is_active']
        #widgets = {
            #'name': forms.TextInput(attrs={'placeholder': 'Enter syllabus name'}),
            #'syllabus_module': forms.TextInput(attrs={'placeholder': 'Enter syllabus module'}),
            #'syllabus_content': forms.Textarea(attrs={'placeholder': 'Enter syllabus content'}),
            #'is_active': forms.CheckboxInput(),
       # }
       # labels = {
            #'name': 'Syllabus Name',
            #'is_active': 'Active',
       # }