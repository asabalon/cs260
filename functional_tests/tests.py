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
			self.selenium.find_element_by_id('id_pet_description')
			self.selenium.find_element_by_id('id_visit_schedule')
			self.selenium.find_element_by_id('id_visit_description')
			self.selenium.find_element_by_id('id_veterinary_physician')
			
			pass
		except NoSuchElementException as e:
			self.fail(e)

	def test_pet_owner_field_is_prefilled(self):
		# No Login capabilities yet; Assume name comes from Database
		try: 
			self.assertFalse(self.selenium.find_element_by_id('id_pet_owner').text is 'Default, Default Default')
			self.assertFalse(self.selenium.find_element_by_id('id_pet_owner').get_attribute('disabled') is 'disabled')
		except NoSuchElementException as e:
			self.fail(e)

	def test_has_date_and_time_picker_widget(self):
		self.fail('Write Test')

	def test_has_navigation_buttons(self):
		self.fail('Finish the Tests')