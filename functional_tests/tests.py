import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        self.selenium.get('%s%s' % (self.live_server_url, '/appointments/add/'))
        self.selenium.implicitly_wait(5)

    # def tearDown(self):
    def test_add_appointment_page_is_accessible(self):
        self.assertIn('Add Appointment', self.selenium.title)

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

        ActionChains(self.selenium).move_to_element(datetime_picker_icon).click(datetime_picker_icon).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bootstrap-datetimepicker-widget'))
            )
            self.assertTrue('display: block' in element.get_attribute('style'))

            active_day = element.find_element_by_class_name('active')
            ActionChains(self.selenium).move_to_element(active_day).click(active_day).perform()
            selected_datetime = self.selenium.find_element_by_id('id_visit_schedule').get_attribute('value')

            self.assertEqual(time.strftime('%m/%d/%Y %I: %p'),
                             time.strftime('%m/%d/%Y %I: %p', time.strptime(selected_datetime, '%m/%d/%Y %I:%M %p')))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

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

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'id_pet_description'))
            )
            self.assertTrue(len(sample_text) > 500)
            self.assertEqual(len(element.get_attribute('value')), 500)
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_pet_description_field_format_constraint(self):
        sample_text = 'Text with ; character'
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_pet_description'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'No Special Characters are allowed in this field')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_visit_description_field_length_constraint(self):
        sample_text = 'Sample Text' * 50
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_description_field = self.selenium.find_element_by_id('id_visit_description')

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'id_visit_description'))
            )
            self.assertTrue(len(sample_text) > 500)
            self.assertEqual(len(element.get_attribute('value')), 500)
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_visit_description_field_format_constraint(self):
        sample_text = 'Text with ; character'
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_description_field = self.selenium.find_element_by_id('id_visit_description')

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).move_to_element(
            submit_button).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_description'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'No Special Characters are allowed in this field')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_format_constraint(self):
        date_text = time.strftime('%Y/%m/%d')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).move_to_element(
            submit_button).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'Enter a valid date/time.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_veterinary_physician_field_behavior(self):
        index = 0
        veterinary_physician_field = self.selenium.find_element_by_id('id_veterinary_physician')
        option_fields = veterinary_physician_field.find_elements_by_tag_name('option')

        for i, option in enumerate(option_fields):
            if (not option.get_attribute('selected')):
                index = i

        ActionChains(self.selenium).move_to_element(veterinary_physician_field).click(
            veterinary_physician_field).move_to_element(option_fields[index]).click(option_fields[index]).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.visibility_of_element_located((By.ID, 'iframe_calendar'))
            )
            self.assertTrue(element.get_attribute('src') is not None)
            self.assertTrue('display: none' not in element.get_attribute('style'))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')
