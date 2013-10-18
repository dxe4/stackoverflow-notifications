__author__ = 'papaloizouc'
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class Scrapper():
    def __init__(self):
        self.driver = webdriver.Firefox()


    def login(self, email, password):
        print("loging in....")
        self.driver.get("http://stackoverflow.com/users/login#log-in")
        element = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_element_by_id("affiliate-signin-iframe"))
        self.driver.switch_to_frame(self.driver.find_element_by_id("affiliate-signin-iframe"))

        emailElement = self.driver.find_element_by_id("email")
        emailElement.send_keys(email)

        passwordElement = self.driver.find_element_by_id("password")
        passwordElement.send_keys(password)

        passwordElement.send_keys(Keys.RETURN)

    def search_tag(self, tag:str):
        print("searching for tag...")
        q = WebDriverWait(self.driver, 15).until(
            lambda driver: driver.find_elements_by_css_selector(".textbox[name=q]"))
        q = q[0]
        q.send_keys("[%s]" % tag)
        q.send_keys(Keys.RETURN)

    def exit_(self):
        print("goodbye see you soon")
        self.driver.close()
        sys.exit(-123)
