from django.test import TestCase
from django.shortcuts import render
from django.http import HttpRequest
from django.forms import ModelForm

from .forms import AppointmentForm

from .models import Customer

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

	def test_correct_uri_resolves_to_add_appointment_page(self):
		self.assertTemplateUsed(self.goto_add_appointment_wo_params(), 'add_appointment.html')

	def test_add_appointment_page_has_form_in_context(self):
		self.assertTrue('form' in self.goto_add_appointment_wo_params().context)

	def test_add_appointment_page_uses_appointment_form(self):
		self.assertTrue(type(self.goto_add_appointment_wo_params().context['form']) is AppointmentForm)

	def test_add_appointment_page_is_a_model_form(self):
		self.assertTrue(isinstance(self.goto_add_appointment_wo_params().context['form'], ModelForm))

	def test_add_appointment_page_forwards_pet_owner_id_after_post(self):
		customer = Customer.objects.create()
		customer.first_name = 'My'
		customer.middle_name = 'First'
		customer.last_name = 'Customer'
		customer.save()

		self.assertEqual(self.goto_add_appointment_with_params({'pet_owner_id' : customer.id}).context['pet_owner_id'], customer.id)



