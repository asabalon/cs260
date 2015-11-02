from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class AddAppointmentTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super(AddAppointmentTests, cls).setUpClass()
		cls.selenium = WebDriver()

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(AddAppointmentTests, cls).tearDownClass()

	def test_add_appointment_page_is_accessible(self):
		self.selenium.get('%s%s' % (self.live_server_url, '/appointments/add'))
		self.assertIn('Add Appointment', self.selenium.title)

	def test_appointment_input_fields_are_present(self):
		self.fail('Finish the Tests')