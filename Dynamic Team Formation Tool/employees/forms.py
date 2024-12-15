from django import forms
from .models import Employee  

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'skills','roll']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skills (comma-separated)'}),
             'roll': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter roll'}),
        }
