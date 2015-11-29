from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium.webdriver.firefox.webdriver import WebDriver


class LogoutTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(LogoutTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LogoutTests, cls).tearDownClass()

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="admin", email="admin@admin.com", password="admin")
        self.c.login(username='admin', password='admin')

        self.selenium.get('%s%s' % (self.live_server_url, '/appointments/login/'))
        self.selenium.find_element_by_name('username').send_keys('admin')
        self.selenium.find_element_by_name('password').send_keys('admin')
        self.selenium.find_element_by_name('btn_submit').click()
        self.selenium.implicitly_wait(10)

    def test_logout_if_in_page(self):
        logout_link = self.selenium.find_element_by_name('lnk_logout').is_displayed()
        self.assertTrue(logout_link)

    def test_logout_goesto_login(self):
        self.selenium.find_element_by_name('lnk_logout').click()
        self.assertEquals(self.selenium.current_url, '%s%s' % (self.live_server_url, '/appointments/login/'))
