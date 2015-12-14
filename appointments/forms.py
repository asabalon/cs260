from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.utils.timezone import localtime, now
from datetime import timedelta
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Reset, HTML
from crispy_forms.bootstrap import FormActions
from .models import Appointment, UserDetails


class AppointmentForm(forms.ModelForm):
    patient_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = ''
    helper.layout = Layout(
        Fieldset(
            'Schedule an Appointment',
            'patient_name',
            'patient',
            'doctor',
            'appointment_date',
        ),
        FormActions(
            Submit('submit', 'Schedule', css_class='btn btn-primary'),
            Reset('reset', 'Clear', css_class='btn btn-default'),
            HTML(
                '<a id="cancel-id-cancel" name="cancel" value="Cancel" class="btn btn btn-default" href="{% url \'appointments:home\' %}">Cancel</a>')
        )
    )

    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient', 'doctor', 'appointment_date']
        widgets = {
            'patient': forms.HiddenInput(attrs={'name': 'patient'}),
            'appointment_date': DateTimePicker(options={
                'format': 'MM/DD/YYYY h:mm a',
                'pickSeconds': False
            }),
            'doctor': forms.Select(
                attrs={'onchange': "change_iframe_src(this.options[this.selectedIndex].value, $('#iframe_calendar'))"})
        }

    class Media:
        js = {'custom/js/form_event_actions.js'}

    def clean_visit_schedule(self):
        sent_datetime = self.cleaned_data['appointment_date']
        current_datetime = localtime(now())
        if (current_datetime - sent_datetime) > timedelta(seconds=1):
            raise forms.ValidationError("Cannot Schedule an Appointment at this Date and Time")
        elif (sent_datetime - current_datetime) < timedelta(days=1):
            raise forms.ValidationError("Kindly give use at least 24 hrs. lead time to schedule your appointment.")
        else:
            pass
        return sent_datetime


class UserDetailsForm(forms.ModelForm):
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True, 'max_length': 30, }),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'required': True, 'max_length': 30, })
    )

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = ''
    helper.layout = Layout(
        Fieldset(
            'Update Your Profile',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'phone_number',
            'mobile_number',
            'address',
        ),
        FormActions(
            Submit('submit', 'Update', css_class='btn btn-primary'),
            Reset('reset', 'Clear', css_class='btn btn-default'),
            HTML(
                '<a id="cancel-id-cancel" name="cancel" value="Cancel" class="btn btn btn-default" href="{% url \'appointments:home\' %}">Cancel</a>')
        )
    )

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number', 'mobile_number', 'address']
        widgets = {
            'patient': forms.HiddenInput(attrs={'name': 'patient'}),
            'date_of_birth': DateTimePicker(options={
                'format': 'MM/DD/YYYY',
                'pickSeconds': False
            }),
            'address': forms.Textarea(),
            'mobile_number': forms.NumberInput,
        }


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(
            attrs={'required': True, 'max_length': 30, 'placeholder': 'Username', 'class': 'form-control'}),
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
        raise forms.ValidationError("Username already exists")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data


class PasswordChangeForm(SetPasswordForm):
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': ("Your old password was entered incorrectly. "
                               "Please enter it again."),
    })
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput)

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
