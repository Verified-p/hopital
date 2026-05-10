from django import forms
from .models import PatientRecord

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = [
            'first_name', 'last_name', 'dob', 'gender', 'phone', 'email', 'address',
            'reason_for_visit', 'medical_history', 'attending_doctor',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
