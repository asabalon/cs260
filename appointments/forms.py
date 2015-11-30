from django import forms
from django.contrib.auth.models import User
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


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(
            attrs={'required': True, 'max_length': 30, 'placeholder': 'UserName', 'class': 'form-control'}),
        error_messages={
            'invalid': "This value must contain only letters, numbers and underscores."},
        label='')
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'required': True, 'max_length': 30, 'placeholder': 'Email', 'class': 'form-control'}),
        label='')
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'required': True, 'max_length': 30, 'render_value': False, 'placeholder': 'Password',
                   'class': 'form-control'}),
        label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'required': True, 'max_length': 30, 'render_value': False, 'placeholder': 'Password (again)',
                   'class': 'form-control'}),
        label='')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("The username already exists. Please try another one.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data
