from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class LoginToKerboodle:

    def __init__(self, credentials, website):

        if website == "backend":
            self.login_url = "https://admin.kerboodle.com/users/login"
        elif website == "frontend":
            self.login_url = "https://www.kerboodle.com/users/login"

        self.credentials = credentials
        self.driver = self.initialise_selenium()
        self.login_to_platform()

    @staticmethod
    def initialise_selenium():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        d = webdriver.Chrome(chrome_options=chrome_options)
        return d

    def enter_credentials(self):
        username = self.driver.find_element_by_id('user_login')
        password = self.driver.find_element_by_id('user_password')
        inst = self.driver.find_element_by_id('user_institution_code')
        username.send_keys(self.credentials['user'])
        password.send_keys(self.credentials['pass'])
        inst.send_keys(self.credentials['inst'])
        self.driver.find_element_by_name('commit').click()

    def login_to_platform(self):
        self.driver.get(self.login_url)
        self.enter_credentials()
        if 'active_session' in self.driver.current_url:
            self.driver.find_element_by_xpath("//a[@href=\"/users/force_login\"]").click()