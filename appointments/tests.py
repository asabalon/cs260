from django.test import TestCase
from django.forms import ModelForm
from .forms import AppointmentForm
from .models import Customer
from .models import Appointment
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Reset, HTML
from django.core.validators import RegexValidator


class AddAppointmentPageTests(TestCase):
    def goto_add_appointment_wo_params(self):
        return self.client.post(
            '/appointments/add/',
            {},
        )

    def goto_add_appointment_with_params(self, dictionary):
        return self.client.post(
            '/appointments/add/',
            dictionary,
        )

    def create_customer(self):
        customer = Customer.objects.create()
        customer.first_name = 'My'
        customer.middle_name = 'First'
        customer.last_name = 'Customer'
        customer.save()

        return customer

    def test_correct_uri_resolves_to_add_appointment_page(self):
        self.assertTemplateUsed(self.goto_add_appointment_wo_params(), 'add_appointment.html')

    def test_add_appointment_page_has_form_in_context(self):
        self.assertTrue('form' in self.goto_add_appointment_wo_params().context)

    def test_add_appointment_page_uses_appointment_form(self):
        self.assertTrue(type(self.goto_add_appointment_wo_params().context['form']) is AppointmentForm)

    def test_add_appointment_form_is_a_model_form(self):
        self.assertTrue(AppointmentForm.__base__ is ModelForm)

    def test_appointment_form_uses_appointment_model(self):
        self.assertTrue(AppointmentForm._meta.model is Appointment)

    def test_appointment_model_refers_to_customer_model(self):
        customer_field = None

        for field in Appointment._meta.get_fields():
            if (field.related_model is Customer):
                customer_field = field
            else:
                continue

        self.assertTrue(customer_field)

    def test_add_appointment_page_forwards_pet_owner_id_after_post(self):
        customer = self.create_customer()

        self.assertEqual(self.goto_add_appointment_with_params({'pet_owner_id': customer.id}).context['pet_owner_id'],
                         customer.id)

    def test_add_appointment_form_contains_pet_owner_name_before_post(self):
        customer = self.create_customer()

        form = self.client.get('/appointments/add/?pet_owner_id=%s' % (customer.id)).context['form']

        self.assertEqual(form['pet_owner_name'].value(), str(customer))

    def test_add_appointment_page_contains_pet_owner_name_after_post(self):
        customer = self.create_customer()

        form = \
            self.goto_add_appointment_with_params(
                {'pet_owner_name': str(customer), 'pet_owner_id': customer.id}).context[
                'form']

        self.assertEqual(form['pet_owner_name'].value(), str(customer))

    def test_form_helper_adds_necessary_buttons(self):
        index = 0
        for i, object in enumerate(AppointmentForm.helper.layout):
            if (type(object) is FormActions):
                index = i
                break

        for button in AppointmentForm.helper.layout[index]:
            if (type(button) is Submit or Reset or HTML):
                continue
            else:
                self.fail("Unrecognized Layout Object")

        self.assertEqual(len(AppointmentForm.helper.layout[index]), 3)

    def test_appointment_model_uses_regex_validator_for_pet_description_field(self):
        index = 0
        validator_list = Appointment._meta.get_field('pet_description').validators
        for i, validator in enumerate(validator_list):
            if (type(validator) is RegexValidator):
                index = i
                break

        self.assertTrue(type(validator_list[index]) is RegexValidator)

    def test_appointment_model_uses_regex_validator_for_visit_description_field(self):
        index = 0
        validator_list = Appointment._meta.get_field('visit_description').validators
        for i, validator in enumerate(validator_list):
            if (type(validator) is RegexValidator):
                index = i
                break

        self.assertTrue(type(validator_list[index]) is RegexValidator)
