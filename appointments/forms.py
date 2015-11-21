from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Appointment
from .models import Customer


class AppointmentForm(forms.ModelForm):
    pet_owner_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = Appointment
        fields = ('pet_owner_name', 'pet_owner', 'pet_description', 'visit_schedule', 'visit_description',
                  'veterinary_physician')
        widgets = {
            'pet_owner': forms.HiddenInput(attrs={'name': 'pet_owner_id'}),
            'visit_schedule': DateTimePicker(options={
                'format': 'YYYY-MM-DD h:mm a',
                'pickSeconds': False
            }),
        }
