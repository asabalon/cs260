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
        self.selenium.implicitly_wait(1)

    def test_appointment_input_fields_are_present(self):
        try:
            self.assertEqual(self.selenium.find_element_by_id('id_pet_description').get_attribute('type'), 'textarea')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_schedule').get_attribute('type'), 'text')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_description').get_attribute('type'), 'textarea')
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
        datetime_picker_widget = self.selenium.find_element_by_class_name('bootstrap-datetimepicker-widget')

        ActionChains(self.selenium).move_to_element(datetime_picker_icon).click(datetime_picker_icon).perform()

        self.assertTrue('display: block' in datetime_picker_widget.get_attribute('style'))

        active_day = datetime_picker_widget.find_element_by_class_name('active')
        ActionChains(self.selenium).move_to_element(active_day).click(active_day).perform()
        selected_datetime = self.selenium.find_element_by_id('id_visit_schedule').get_attribute('value')

        self.assertEqual(time.strftime("%Y-%m-%d %I: %p"),
                         time.strftime("%Y-%m-%d %I: %p", time.strptime(selected_datetime, "%Y-%m-%d %I:%M %p")))

    def test_has_navigation_buttons(self):
        try:
            self.assertEqual(self.selenium.find_element_by_id('submit-id-submit').get_attribute('type'), 'submit')
            self.assertEqual(self.selenium.find_element_by_id('reset-id-reset').get_attribute('type'), 'reset')
            self.assertTrue(self.selenium.find_element_by_id('cancel-id-cancel').get_attribute('href') is not None)
        except NoSuchElementException as e:
            self.fail(e)

    def test_submit_button_redirects_to_add_appointment_page(self):
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        ActionChains(self.selenium).move_to_element(submit_button).click(submit_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, '/appointments/add/'))

    def test_clear_button_clears_input_(self):
        cancel_button = self.selenium.find_element_by_id('reset-id-reset')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, 'Test Text').move_to_element(
            cancel_button).click(cancel_button).perform()

        self.assertEqual(pet_description_field.get_attribute('value'), '')

    # No Homepage capabilities yet; Redirects to Add Appointment Page
    def test_cancel_button_redirects_to_expected_page(self):
        cancel_button = self.selenium.find_element_by_id('cancel-id-cancel')
        ActionChains(self.selenium).move_to_element(cancel_button).click(cancel_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, '/appointments/add/'))

    def test_pet_description_field_length_constraint(self):
        sample_text = 'Sample Text' * 50
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        new_pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        self.assertTrue(len(sample_text) > 500)
        self.assertEqual(len(new_pet_description_field.get_attribute('value')), 500)

    def test_pet_description_field_format_constraint(self):
        sample_text = 'Text with ; character'
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        new_pet_description_error = self.selenium.find_element_by_id('error_1_id_pet_description')

        self.assertEqual(new_pet_description_error.find_element_by_tag_name('strong').text,
                         'No Special Characters are allowed in this field')

    def test_visit_description_field_length_constraint(self):
        sample_text = 'Sample Text' * 50
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_description_field = self.selenium.find_element_by_id('id_visit_description')

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        new_visit_description_field = self.selenium.find_element_by_id('id_visit_description')

        self.assertTrue(len(sample_text) > 500)
        self.assertEqual(len(new_visit_description_field.get_attribute('value')), 500)

    def test_visit_description_field_format_constraint(self):
        self.fail('Finish the Tests')