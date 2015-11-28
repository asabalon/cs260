from django import forms
from django.utils.timezone import localtime, now
from datetime import timedelta
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Reset, HTML
from crispy_forms.bootstrap import FormActions
from .models import Pet, Appointment


class AppointmentForm(forms.ModelForm):
    pet_owner_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = 'add_appointment'
    helper.layout = Layout(
        Fieldset(
            'Schedule an Appointment',
            'pet_owner_name',
            'pet_name',
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
        fields = ['pet_owner', 'pet_name', 'pet_description', 'visit_schedule', 'visit_description',
                  'veterinary_physician']
        widgets = {
            'pet_owner': forms.HiddenInput(attrs={'name': 'pet_owner_id'}),
            'pet_description': forms.Textarea(),
            'visit_description': forms.Textarea(),
            'visit_schedule': DateTimePicker(options={
                'format': 'MM/DD/YYYY h:mm a',
                'pickSeconds': False
            }),
            'veterinary_physician': forms.Select(
                attrs={'onchange': "change_iframe_src(this.options[this.selectedIndex].value, $('#iframe_calendar'))"})
        }

    class Media:
        js = {'custom/js/form_event_actions.js'}

    def clean_visit_schedule(self):
        sent_datetime = self.cleaned_data['visit_schedule']
        current_datetime = localtime(now())
        if (current_datetime - sent_datetime) > timedelta(seconds=1):
            raise forms.ValidationError("Cannot Schedule an Appointment at this Date and Time")
        elif (sent_datetime - current_datetime) < timedelta(days=1):
            raise forms.ValidationError("Kindly give use at least 24 hrs. lead time to schedule your appointment.")
        else:
            pass
        return sent_datetime
