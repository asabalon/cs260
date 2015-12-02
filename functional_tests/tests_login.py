from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(LoginTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LoginTests, cls).tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/appointments/login/'))
        self.selenium.implicitly_wait(3)

    def test_login_is_running(self):
        response = self.client.get(reverse('appointments:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_is_accessible(self):
        self.assertIn('Login', self.selenium.title)

    def test_login_invalidparameter_shouldreturn_errormessage(self):
        self.selenium.find_element_by_name('username').send_keys('zxa')
        self.selenium.find_element_by_name('password').send_keys('xxx')
        self.selenium.find_element_by_name('btn_submit').click()
        self.selenium.implicitly_wait(3)

        self.assertEqual(self.selenium.find_element_by_name('state').text, 'Username/Password is incorrect')
