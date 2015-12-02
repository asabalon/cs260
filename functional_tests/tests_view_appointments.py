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


class ViewAppointmentsTests(StaticLiveServerTestCase):
    LOGIN_URI = '/appointments/login/'
    LOGOUT_URI = '/appointments/logout/'
    ADD_APPOINTMENT_URI = '/appointments/add/'
    VIEW_APPOINTMENTS_URI = '/appointments/view/'

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(
            EC.staleness_of(old_page)
        )

    @classmethod
    def setUpClass(cls):
        super(ViewAppointmentsTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ViewAppointmentsTests, cls).tearDownClass()

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
            self.selenium.get('%s%s' % (self.live_server_url, self.VIEW_APPOINTMENTS_URI))

    def tearDown(self):
        with self.wait_for_page_load():
            self.selenium.get('%s%s' % (self.live_server_url, self.LOGOUT_URI))

    # No Pet and Veterinary Registration Features yet
    def create_test_data(self):
        pet_params = '?name=Doggy&breed=Pug&age=1'
        veterinary_physician_params = '?username=veterinary_physician&first_name=Dr&middle_name=Veterinary&last_name=Physician&email=cs2602015project@gmail.com'

        with self.wait_for_page_load():
            self.selenium.get(
                '%s%s%s%s' % (
                    self.live_server_url, self.ADD_APPOINTMENT_URI, 'create_test_vet/', veterinary_physician_params))

        with self.wait_for_page_load():
            self.selenium.get('%s%s%s%s' % (
                self.live_server_url, self.ADD_APPOINTMENT_URI, 'create_test_pet/', pet_params))

        with self.wait_for_page_load():
            self.selenium.get(
                '%s%s' % (self.live_server_url, self.ADD_APPOINTMENT_URI))

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

        with self.wait_for_page_load():
            self.selenium.get(
                '%s%s' % (self.live_server_url, self.VIEW_APPOINTMENTS_URI))

        return {'scheduled_visit': current_datetime}

    def test_view_appointments_page_is_accessible(self):
        # No HTTP Response yet on Selenium WebDriver
        response = requests.get(self.selenium.current_url)

        self.assertEqual(response.status_code, 200)

    def test_view_appointments_page_contains_error_message_when_no_appointments(self):
        error_message = self.selenium.find_element_by_class_name('alert-danger')

        self.assertEqual(error_message.text, 'No Appointments yet. Click here to schedule an appointment.')

    def test_view_appointments_page_contains_info_message_when_with_appointments(self):
        self.create_test_data()
        info_message = self.selenium.find_element_by_class_name('alert-info')

        self.assertEqual(info_message.text, 'Regularly check the status of your appointments.')

    def test_view_appointments_page_is_in_tabular_form(self):
        self.create_test_data()
        appointments_table_by_class = self.selenium.find_element_by_class_name('table')
        appointments_table_by_tagname = self.selenium.find_element_by_tag_name('table')

        self.assertEqual(appointments_table_by_class, appointments_table_by_tagname)

    def test_view_appointments_page_contains_headers(self):
        self.create_test_data()
        expected_table_headers = {'#', 'Pet Name', 'Doctor\'s Name', 'Schedule', 'Status'}
        appointments_table = self.selenium.find_element_by_class_name('table')
        appointments_table_headers = appointments_table.find_elements(By.XPATH, "//thead/tr/th")

        self.assertEqual(len(expected_table_headers), len(appointments_table_headers))
        for header in appointments_table_headers:
            self.assertTrue(header.text in expected_table_headers)

    def test_view_appointments_page_contains_correct_data(self):
        response = self.create_test_data()

        expected_table_data = {'Doggy', 'Physician, Dr. Veterinary', response.get('scheduled_visit'),
                                  'Waiting Confirmation'}
        appointments_table = self.selenium.find_element_by_class_name('table')
        appointments_table_data = appointments_table.find_elements(By.XPATH, "//tbody/tr[0]/td")

        for header in appointments_table_data:
            self.assertTrue(header.text in expected_table_data)

    def test_view_appointments_page_contains_headers_in_correct_order(self):
        self.create_test_data()
        expected_table_headers = ['#', 'Pet Name', 'Doctor\'s Name', 'Schedule', 'Status']
        appointments_table = self.selenium.find_element_by_class_name('table')
        appointments_table_headers = appointments_table.find_elements(By.XPATH, "//thead/tr/th")

        self.assertEqual(len(expected_table_headers), len(appointments_table_headers))
        for i, header in enumerate(appointments_table_headers):
            self.assertEqual(header.text, expected_table_headers[i])

    def test_view_appointments_page_contains_correct_data_in_order(self):
        response = self.create_test_data()

        expected_table_data = ['Doggy', 'Physician, Dr. Veterinary', response.get('scheduled_visit'),
                                  'Waiting Confirmation']
        appointments_table = self.selenium.find_element_by_class_name('table')
        appointments_table_data = appointments_table.find_elements(By.XPATH, "//tbody/tr[0]/td")

        for i, header in enumerate(appointments_table_data):
            self.assertTrue(header.text, expected_table_data[i])
