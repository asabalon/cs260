import time, requests
from contextlib import contextmanager
from datetime import timedelta, datetime
from django.utils.timezone import localtime, now
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import select, expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appointments.models import Customer


class AddAppointmentTests(StaticLiveServerTestCase):
    LOGIN_URI = '/appointments/login/'
    LOGOUT_URI = '/appointments/logout/'
    APPOINTMENT_URI = '/appointments/add/'

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(
            EC.staleness_of(old_page)
        )

    @classmethod
    def setUpClass(cls):
        super(AddAppointmentTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(AddAppointmentTests, cls).tearDownClass()

    def setUp(self):
        customer = Customer.objects.create_user('temp_username', 'temporary@email.com', 'temp_password',
                                                first_name='My',
                                                middle_name='First', last_name='Customer')
        customer.save()

        self.selenium.get('%s%s' % (self.live_server_url, self.LOGIN_URI))

        with self.wait_for_page_load():
            login_button = self.selenium.find_element_by_class_name('btn-primary')
            username_field = self.selenium.find_element_by_id('inputUsername')
            password_field = self.selenium.find_element_by_id('inputPassword')

            ActionChains(self.selenium).send_keys_to_element(username_field, 'temp_username').send_keys_to_element(
                password_field, 'temp_password').click(login_button).perform()

        with self.wait_for_page_load():
            self.selenium.get('%s%s%s%s' % (self.live_server_url, self.APPOINTMENT_URI, '?pet_owner=', customer.id))

    def tearDown(self):
        with self.wait_for_page_load():
            self.selenium.get('%s%s' % (self.live_server_url, self.LOGOUT_URI))

    # No Pet and Veterinary Registration Features yet
    def create_test_data(self):
        customer = Customer.objects.get(username='temp_username')
        pet_params = '?name=Doggy&breed=Pug&age=1&owner='
        veterinary_physician_params = '?username=veterinary_physician&first_name=Dr&middle_name=Veterinary&last_name=Physician&email=cs2602015project@gmail.com'

        with self.wait_for_page_load():
            self.selenium.get(
                '%s%s%s%s' % (
                    self.live_server_url, self.APPOINTMENT_URI, 'create_test_vet/', veterinary_physician_params))

        with self.wait_for_page_load():
            self.selenium.get('%s%s%s%s%s' % (
                self.live_server_url, self.APPOINTMENT_URI, 'create_test_pet/', pet_params, customer.id))

        with self.wait_for_page_load():
            self.selenium.get(
                '%s%s%s%s' % (self.live_server_url, self.APPOINTMENT_URI, '?pet_owner=', customer.id))

    def test_add_appointment_page_is_accessible(self):
        # No HTTP Response yet on Selenium WebDriver
        response = requests.get(self.selenium.current_url)

        self.assertEqual(response.status_code, 200)

    def test_appointment_input_fields_are_present(self):
        try:
            pet_name_field = self.selenium.find_element_by_id('id_pet_name')
            pet_description_field = self.selenium.find_element_by_id('id_pet_description')
            visit_schedule_field = self.selenium.find_element_by_id('id_visit_schedule')
            visit_description_field = self.selenium.find_element_by_id('id_visit_description')
            veterinary_physician_field = self.selenium.find_element_by_id('id_veterinary_physician')

            self.assertEqual(pet_name_field.get_attribute('type'), 'select-one')
            self.assertEqual(pet_description_field.get_attribute('type'), 'textarea')
            self.assertEqual(visit_schedule_field.get_attribute('type'), 'text')
            self.assertEqual(visit_description_field.get_attribute('type'), 'textarea')
            self.assertEqual(veterinary_physician_field.get_attribute('type'),
                             'select-one')
        except NoSuchElementException as e:
            self.fail(e)

    def test_pet_owner_field_is_prefilled(self):
        self.create_test_data()
        pet_owner_name_field = self.selenium.find_element_by_id('id_pet_owner_name')

        self.assertEqual(pet_owner_name_field.get_attribute('value'), 'Customer, My First')
        self.assertTrue(pet_owner_name_field.get_attribute('readonly'))

    def test_has_date_and_time_picker_widget(self):
        datetime_picker_icon = self.selenium.find_element_by_class_name('glyphicon-calendar')

        ActionChains(self.selenium).click(datetime_picker_icon).perform()

        try:
            datetime_picker_widget = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bootstrap-datetimepicker-widget'))
            )
            active_day = datetime_picker_widget.find_element_by_class_name('active')

            ActionChains(self.selenium).click(active_day).perform()

            selected_datetime = self.selenium.find_element_by_id('id_visit_schedule').get_attribute('value')
            self.assertTrue(datetime_picker_widget.is_displayed())
            self.assertEqual(time.strftime('%m/%d/%Y %I: %p'),
                             time.strftime('%m/%d/%Y %I: %p', time.strptime(selected_datetime, '%m/%d/%Y %I:%M %p')))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_has_navigation_buttons(self):
        try:
            clear_button = self.selenium.find_element_by_id('reset-id-reset')
            submit_button = self.selenium.find_element_by_id('submit-id-submit')
            cancel_button = self.selenium.find_element_by_id('cancel-id-cancel')

            self.assertEqual(submit_button.get_attribute('type'), 'submit')
            self.assertEqual(clear_button.get_attribute('type'), 'reset')
            self.assertTrue(cancel_button.get_attribute('href') is not None)
        except NoSuchElementException as e:
            self.fail(e)

    def test_submit_button_redirects_to_add_appointment_page(self):
        submit_button = self.selenium.find_element_by_id('submit-id-submit')

        ActionChains(self.selenium).click(submit_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, self.APPOINTMENT_URI))

    def test_clear_button_clears_input(self):
        clear_button = self.selenium.find_element_by_id('reset-id-reset')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, 'Test Text').click(
            clear_button).perform()

        self.assertEqual(pet_description_field.get_attribute('value'), '')

    # No Homepage capabilities yet; Redirects to Add Appointment Page
    def test_cancel_button_redirects_to_expected_page(self):
        cancel_button = self.selenium.find_element_by_id('cancel-id-cancel')

        ActionChains(self.selenium).click(cancel_button).perform()

        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, self.APPOINTMENT_URI))

    def test_pet_description_field_length_constraint(self):
        sample_text = 'Sample Text' * 50
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).click(
            submit_button).perform()

        try:
            new_pet_description_field = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'id_pet_description'))
            )

            self.assertTrue(len(sample_text) > 500)
            self.assertEqual(len(new_pet_description_field.get_attribute('value')), 500)
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_pet_description_field_format_constraint(self):
        sample_text = 'Text with ; character'
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        pet_description_field = self.selenium.find_element_by_id('id_pet_description')

        ActionChains(self.selenium).send_keys_to_element(pet_description_field, sample_text).click(
            submit_button).perform()

        try:
            pet_description_error = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_pet_description'))
            )

            self.assertEqual(pet_description_error.find_element_by_tag_name('strong').text,
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
            new_visit_description_field = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'id_visit_description'))
            )

            self.assertTrue(len(sample_text) > 500)
            self.assertEqual(len(new_visit_description_field.get_attribute('value')), 500)
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_visit_description_field_format_constraint(self):
        sample_text = 'Text with ; character'
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_description_field = self.selenium.find_element_by_id('id_visit_description')

        ActionChains(self.selenium).send_keys_to_element(visit_description_field, sample_text).click(
            submit_button).perform()

        try:
            visit_description_error = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_description'))
            )

            self.assertEqual(visit_description_error.find_element_by_tag_name('strong').text,
                             'No Special Characters are allowed in this field')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_past_time_validation(self):
        date_text = format(datetime.now() - timedelta(hours=1), '%m/%d/%Y %I:%M %p')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).click(submit_button).perform()

        try:
            visit_schedule_error = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )

            self.assertEqual(visit_schedule_error.find_element_by_tag_name('strong').text,
                             'Cannot Schedule an Appointment at this Date and Time')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_scheduled_visit_field_lead_time_validation(self):
        date_text = format(localtime(now()) + timedelta(hours=1), '%m/%d/%Y %I:%M %p')
        submit_button = self.selenium.find_element_by_id('submit-id-submit')
        visit_schedule_field = self.selenium.find_element_by_name('visit_schedule')

        ActionChains(self.selenium).send_keys_to_element(visit_schedule_field, date_text).click(submit_button).perform()

        try:
            visit_schedule_error = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )

            self.assertEqual(visit_schedule_error.find_element_by_tag_name('strong').text,
                             'Kindly give use at least 24 hrs. lead time to schedule your appointment.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_veterinary_physician_field_behavior(self):
        self.create_test_data()
        index = 0
        veterinary_physician_field = self.selenium.find_element_by_id('id_veterinary_physician')
        vet_option_fields = veterinary_physician_field.find_elements_by_tag_name('option')

        for i, option in enumerate(vet_option_fields):
            if (not option.get_attribute('selected')):
                index = i

        select_box = select.Select(veterinary_physician_field)
        select_box.select_by_value(vet_option_fields[index].get_attribute('value'))

        try:
            calendar_widget = WebDriverWait(self.selenium, 20).until(
                EC.visibility_of_element_located((By.ID, 'iframe_calendar'))
            )

            self.assertTrue(calendar_widget.get_attribute('src') is not None)
            self.assertTrue('display: none' not in calendar_widget.get_attribute('style'))
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')

    def test_appointment_page_form_checking(self):
        webDriverWait = WebDriverWait(self.selenium, 10)
        submit_button = self.selenium.find_element_by_id('submit-id-submit')

        ActionChains(self.selenium).click(submit_button).perform()

        try:
            pet_name_error = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_pet_name'))
            )
            visit_schedule_error = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_schedule'))
            )
            visit_description_error = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_visit_description'))
            )
            veterinary_physician_error = webDriverWait.until(
                EC.presence_of_element_located((By.ID, 'error_1_id_veterinary_physician'))
            )

            self.assertEqual(pet_name_error.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(visit_schedule_error.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(visit_description_error.find_element_by_tag_name('strong').text,
                             'This field is required.')
            self.assertEqual(veterinary_physician_error.find_element_by_tag_name('strong').text,
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
            pet_name_field = self.selenium.find_element_by_id('id_pet_name')
            pet_option_fields = pet_name_field.find_elements_by_tag_name('option')
            pet_description_field = self.selenium.find_element_by_id('id_pet_description')
            visit_schedule_field = self.selenium.find_element_by_id('id_visit_schedule')
            visit_description_field = self.selenium.find_element_by_id('id_visit_description')
            veterinary_physician_field = self.selenium.find_element_by_id('id_veterinary_physician')
            vet_option_fields = veterinary_physician_field.find_elements_by_tag_name('option')

            for i, option in enumerate(vet_option_fields):
                if (option.get_attribute('selected') is None):
                    vet_index = i

            for i, option in enumerate(pet_option_fields):
                if (option.get_attribute('selected') is None):
                    pet_index = i

            vet_select_box = select.Select(veterinary_physician_field)
            vet_select_box.select_by_value(vet_option_fields[vet_index].get_attribute('value'))

            pet_select_box = select.Select(pet_name_field)
            pet_select_box.select_by_value(pet_option_fields[pet_index].get_attribute('value'))

            current_datetime = format(datetime.now() + timedelta(hours=25), '%m/%d/%Y %I:%M %p')

            actions = ActionChains(self.selenium)
            actions.send_keys_to_element(pet_description_field, 'Siberian Husky')
            actions.send_keys_to_element(visit_schedule_field, current_datetime)
            actions.send_keys_to_element(visit_description_field, 'Checkup')
            actions.click(submit_button)
            actions.perform()

            success_message = webDriverWait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
            )

            self.assertEqual(success_message.text,
                             'Your request for an Appointment has been saved. Please wait for the Physician\'s Confirmation via email.')
        except TimeoutException as e:
            self.fail('Unable to Execute Test Properly')
