from django.test import TestCase

class AddAppointmentPageTests(TestCase):

	def test_correct_uri_resolves_to_add_appointment_page(self):
		response = self.client.post(
			'/appointments/add/',
			{},
		)

		self.assertTemplateUsed(response, 'add_appointment.html')
		
