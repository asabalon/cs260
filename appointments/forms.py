from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Reset, HTML
from crispy_forms.bootstrap import FormActions
from .models import Appointment
from .urls import urlpatterns


class AppointmentForm(forms.ModelForm):
    pet_owner_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = 'add_appointment'
    helper.layout = Layout(
        Fieldset(
            'Schedule an Appointment',
            'pet_owner_name',
            'pet_owner',
            'pet_description',
            'visit_schedule',
            'visit_description',
            'veterinary_physician'
        ),
        FormActions(
            Submit('submit', 'Schedule', css_class='btn btn-primary'),
            Reset('reset', 'Clear', css_class='btn btn-default'),
            HTML(
                '<a id="cancel-id-cancel" name="cancel" value="Cancel" class="btn btn btn-default" href="{% url "add_appointment" %}">Cancel</a>')
        )
    )

    class Meta:
        model = Appointment
        fields = ['pet_owner', 'pet_description', 'visit_schedule', 'visit_description', 'veterinary_physician']
        widgets = {
            'pet_owner': forms.HiddenInput(attrs={'name': 'pet_owner_id'}),
            'visit_schedule': DateTimePicker(options={
                'format': 'YYYY-MM-DD h:mm a',
                'pickSeconds': False
            }),
        }
