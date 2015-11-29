import time, json
from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.utils.timezone import localtime, now
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import select, expected_conditions as EC


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
        self.c = Client()
        self.user = User.objects.create_user(username="admin", email="admin@admin.com", password="admin")
        self.c.login(username='admin', password='admin')

        self.selenium.get('%s%s' % (self.live_server_url, '/appointments/login/'))
        self.selenium.find_element_by_name('username').send_keys('admin')
        self.selenium.find_element_by_name('password').send_keys('admin')
        self.selenium.find_element_by_name('btn_submit').click()
        self.selenium.implicitly_wait(10)

    def create_test_data(self):
        pet_params = '?name=Doggy&breed=Pug&age=1&owner='
        customer_params = '?first_name=My&middle_name=First&last_name=Customer'
        veterinary_physician_params = '?first_name=Dr&middle_name=Veterinary&last_name=Physician&email=cs2602015project@gmail.com'

        try:
            self.selenium.get(
                '%s%s%s' % (self.live_server_url, '/appointments/add/create_test_vet/', veterinary_physician_params))
            self.selenium.get(
                '%s%s%s' % (self.live_server_url, '/appointments/add/create_test_customer/', customer_params))

            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'pre'))
            )

            response = json.loads(element.text)

            self.selenium.get('%s%s%s%s' % (
                self.live_server_url, '/appointments/add/create_test_pet/', pet_params, response['pet_owner_id']))
            self.selenium.get(
                '%s%s%s' % (self.live_server_url, '/appointments/add/?pet_owner=', response['pet_owner_id']))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_add_appointment_page_is_accessible(self):
        response = self.c.get(reverse('add_appointment'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_input_fields_are_present(self):
        try:
            self.assertEqual(self.selenium.find_element_by_id('id_pet_name').get_attribute('type'), 'select-one')
            self.assertEqual(self.selenium.find_element_by_id('id_pet_description').get_attribute('type'), 'textarea')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_schedule').get_attribute('type'), 'text')
            self.assertEqual(self.selenium.find_element_by_id('id_visit_description').get_attribute('type'), 'textarea')
            self.assertEqual(self.selenium.find_element_by_id('id_veterinary_physician').get_attribute('type'),
                             'select-one')
        except NoSuchElementException as e:
            self.fail(e)

    def test_pet_owner_field_is_prefilled(self):
        self.create_test_data()
        # No Login capabilities yet; Assume name comes from Database
        self.assertEqual(
            self.selenium.find_element_by_id('id_pet_owner_name').get_attribute('value'), 'Customer, My First')
        self.assertTrue(self.selenium.find_element_by_id('id_pet_owner_name').get_attribute('readonly'))

    def test_has_date_and_time_picker_widget(self):
        datetime_picker_icon = self.selenium.find_element_by_class_name('glyphicon-calendar')

        ActionChains(self.selenium).click(datetime_picker_icon).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bootstrap-datetimepicker-widget'))
            )
            self.assertTrue('display: block' in element.get_attribute('style'))

            active_day = element.find_element_by_class_name('active')
            ActionChains(self.selenium).click(active_day).perform()
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

        ActionChains(self.selenium).click(submit_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, '/appointments/add/'))

    def test_clear_button_clears_input_(self):
        cancel_button = self.selenium.find_element_by_id('reset-id-reset')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, 'Test Text').click(
            cancel_button).perform()

        self.assertEqual(pet_description_field.get_attribute('value'), '')

    # No Homepage capabilities yet; Redirects to Add Appointment Page
    def test_cancel_button_redirects_to_expected_page(self):
        cancel_button = self.selenium.find_element_by_id('cancel-id-cancel')

        ActionChains(self.selenium).click(cancel_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, '/appointments/add/'))

    def test_pet_description_field_length_constraint(self):
        sample_text = 'Sample Text' * 50
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).click(
            submit_button).perform()

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

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).click(
            submit_button).perform()

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

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).click(
            submit_button).perform()

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

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).click(
            submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_description'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'No Special Characters are allowed in this field')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_format_completion_for_time(self):
        date_text = format(datetime.now() + timedelta(hours=25), '%I:%M %p')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'Cannot Schedule an Appointment at this Date and Time')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_format_completion_for_date(self):
        date_text = format(datetime.now() + timedelta(hours=25), '%m/%d/%Y')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'Kindly give use at least 24 hrs. lead time to schedule your appointment.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_lead_time_validation(self):
        date_text = format(localtime(now()) + timedelta(hours=1), '%m/%d/%Y %I:%M %p')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).click(submit_button).perform()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            self.assertEqual(element.find_element_by_tag_name('strong').text,
                             'Kindly give use at least 24 hrs. lead time to schedule your appointment.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_veterinary_physician_field_behavior(self):
        self.create_test_data()
        index = 0
        veterinary_physician = self.selenium.find_element_by_id('id_veterinary_physician')
        option_fields = veterinary_physician.find_elements_by_tag_name('option')

        for i, option in enumerate(option_fields):
            if (not option.get_attribute('selected')):
                index = i

        select_box = select.Select(veterinary_physician)
        select_box.select_by_value(option_fields[index].get_attribute('value'))

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.visibility_of_element_located((By.ID, 'iframe_calendar'))
            )
            self.assertTrue(element.get_attribute('src') is not None)
            self.assertTrue('display: none' not in element.get_attribute('style'))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_appointment_page_form_checking(self):
        webDriverWait = WebDriverWait(self.selenium, 10)
        submit_button = self.selenium.find_element_by_id('submit-id-submit')

        ActionChains(self.selenium).click(submit_button).perform()

        try:
            pet_name = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_pet_name'))
            )
            visit_schedule = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            visit_description = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_description'))
            )
            veterinary_physician = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_veterinary_physician'))
            )

            self.assertEqual(pet_name.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(visit_schedule.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(visit_description.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(veterinary_physician.find_element_by_tag_name('strong').text,
                             'This field is required.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_successful_appointment_scheduling(self):
        self.create_test_data()
        webDriverWait = WebDriverWait(self.selenium, 10)

        try:
            vet_index = 0
            pet_index = 0
            submit_button = self.selenium.find_element_by_id('submit-id-submit')
            pet_name = self.selenium.find_element_by_id('id_pet_name')
            pet_option_fields = pet_name.find_elements_by_tag_name('option')
            pet_description = self.selenium.find_element_by_id('id_pet_description')
            visit_schedule = self.selenium.find_element_by_id('id_visit_schedule')
            visit_description = self.selenium.find_element_by_id('id_visit_description')
            veterinary_physician = self.selenium.find_element_by_id('id_veterinary_physician')
            vet_option_fields = veterinary_physician.find_elements_by_tag_name('option')

            for i, option in enumerate(vet_option_fields):
                if (option.get_attribute('selected') is None):
                    vet_index = i

            for i, option in enumerate(pet_option_fields):
                if (option.get_attribute('selected') is None):
                    pet_index = i

            vet_select_box = select.Select(veterinary_physician)
            vet_select_box.select_by_value(vet_option_fields[vet_index].get_attribute('value'))

            pet_select_box = select.Select(pet_name)
            pet_select_box.select_by_value(pet_option_fields[pet_index].get_attribute('value'))

            current_datetime = format(datetime.now() + timedelta(hours=25), '%m/%d/%Y %I:%M %p')

            actions = ActionChains(self.selenium)
            actions.send_keys_to_element(pet_description, 'Siberian Husky')
            actions.send_keys_to_element(visit_schedule, current_datetime)
            actions.send_keys_to_element(visit_description, 'Checkup')
            actions.click(submit_button)
            actions.perform()

            element = webDriverWait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
            )
            self.assertEqual(element.text,
                             'Your request for an Appointment has been saved. Please wait for the Physician\'s Confirmation via email.')

        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')
