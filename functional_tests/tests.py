import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
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

    # def tearDown(self):

    def test_add_appointment_page_is_accessible(self):
        self.assertIn('Add Appointment', self.selenium.title)

    def test_appointment_input_fields_are_present(self):
        try:
            self.assertEqual(self.selenium.find_element_by_id('id_pet_description').get_attribute('type'), 'text')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_schedule').get_attribute('type'), 'text')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_description').get_attribute('type'), 'text')
            self.assertEqual(self.selenium.find_element_by_id('id_veterinary_physician').get_attribute('type'),
                             'select-one')
        except NoSuchElementException as e:
            self.fail(e)

    def test_pet_owner_field_is_prefilled(self):
        # No Login capabilities yet; Assume name comes from Database
        self.assertEqual(
            self.selenium.find_element_by_id('id_pet_owner_name').get_attribute('value'), 'Default, Default Default')
        self.assertTrue(self.selenium.find_element_by_id('id_pet_owner_name').get_attribute('readonly'))

    def test_has_date_and_time_picker_widget(self):
        datetime_picker_icon = self.selenium.find_element_by_class_name('glyphicon-calendar')
        ActionChains(self.selenium).move_to_element(datetime_picker_icon).click(datetime_picker_icon).perform()

        datetime_picker_widget = self.selenium.find_element_by_class_name('bootstrap-datetimepicker-widget')
        self.assertTrue('display: block' in datetime_picker_widget.get_attribute('style'))

        active_day = datetime_picker_widget.find_element_by_class_name('active')
        ActionChains(self.selenium).move_to_element(active_day).click(active_day).perform()
        selected_datetime = self.selenium.find_element_by_id('id_visit_schedule').get_attribute('value')

        self.assertEqual(time.strftime("%Y-%m-%d %I:%M %p"),
                         time.strftime("%Y-%m-%d %I:%M %p", time.strptime(selected_datetime, "%Y-%m-%d %I:%M %p")))

    def test_has_navigation_buttons(self):
        self.fail('Finish the Tests')
