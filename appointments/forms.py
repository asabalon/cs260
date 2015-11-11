from django import forms

from .models import Appointment

class AppointmentForm(forms.ModelForm):	
	class Meta:
		model = Appointment
		fields = ['pet_owner', 'pet_description', 'visit_schedule', 'visit_description', 'veterinary_physician']
		widgets = {
            'pet_owner': forms.Select(attrs={'disabled':'disabled'})
        }