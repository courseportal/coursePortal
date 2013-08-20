from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class MySeleniumTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()
    
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("email")
        username_input.send_keys('tyan@umich.edu')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1111')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()



