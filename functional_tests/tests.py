from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class AddAppointmentTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super(AddAppointmentTests, cls).setUpClass()
		cls.selenium = WebDriver()

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(AddAppointmentTests, cls).tearDownClass()

	def setUp(self):
		self.selenium.get('%s%s' % (self.live_server_url, '/appointments/add'))

	#def tearDown(self):

	def test_add_appointment_page_is_accessible(self):
		self.assertIn('Add Appointment', self.selenium.title)

	def test_appointment_input_fields_are_present(self):
		try: 
			self.selenium.find_element_by_id('id_pet_desc')
			self.selenium.find_element_by_id('id_visit_desc')
			self.selenium.find_element_by_id('id_visit_sched')
			self.selenium.find_element_by_id('id_vet_physician')
			
			pass
		except NoSuchElementException as e:
			self.fail(e)

	def test_pet_owner_field_is_prefilled(self):
		self.fail('Finish the Tests')