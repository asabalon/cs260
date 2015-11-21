from django.test import TestCase
from django.shortcuts import render
from django.http import HttpRequest
from django.forms import ModelForm
from .forms import AppointmentForm
from .models import Customer
from .models import Appointment


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
        for field in Appointment._meta.get_fields():
            if (field.related_model is Customer):
                pass
            else:
                continue

        self.fail("No Customer Model Field Found")

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
