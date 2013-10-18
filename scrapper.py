__author__ = 'papaloizouc'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

EMAIL = ""
PASSWORD = ""


class Scrapper():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.login(EMAIL, PASSWORD)
        self.search_tag("python")

    def login(self, email, password):
        self.driver.get("http://stackoverflow.com/users/login#log-in")
        element = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_id("affiliate-signin-iframe"))
        self.driver.switch_to_frame(self.driver.find_element_by_id("affiliate-signin-iframe"))

        email = self.driver.find_element_by_id("email")
        email.send_keys(EMAIL)

        password = self.driver.find_element_by_id("password")
        password.send_keys(PASSWORD)

        password.send_keys(Keys.RETURN)

    def search_tag(self, tag:str):
        q = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_elements_by_css_selector(".textbox[name=q]"))
        q = q[0]
        q.send_keys("[%s]" % tag)
        q.send_keys(Keys.RETURN)

    def exit(self):
        self.driver.close()

