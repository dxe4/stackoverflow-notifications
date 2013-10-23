__author__ = 'papaloizouc'
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from bs4 import BeautifulSoup
from bs4.element import Tag
from model import User, Question, Model
from ui import View
from selenium.selenium import selenium

QUESTION = "[id^=question-summary-]"
QUESTION_TITLE = ".question-hyperlink"
USER_NAME = ".user-details [href^=/users/]"
REPUTATION = ".reputation-score"
TAG = ".post-tag"
VOTES = ".vote-count-post strong"
ANSWERS = ".status strong"
VIEWS = ".views"
WEBSITE = "http://www.stackoverflow.com"
TIME = ".relativetime"


class Scrapper():
    def __init__(self,model:Model,view:View):
        self.driver = webdriver.Firefox()
        self.model = model

    def login(self, email, password):
        print("logging in.... %s " % (email))
        self.driver.get(WEBSITE + "/users/login#log-in")
        frame = self.wait_for(15, lambda driver: driver.find_element_by_id("affiliate-signin-iframe"))
        self.driver.switch_to_frame(frame)

        emailElement = self.driver.find_element_by_id("email")
        emailElement.send_keys(email)

        passwordElement = self.driver.find_element_by_id("password")
        passwordElement.send_keys(password)
        passwordElement.send_keys(Keys.RETURN)

    def search_tag(self, tag:str):
        print("searching for tag... %s" % (tag))
        q = self.wait_for(15, lambda driver: driver.find_elements_by_css_selector(".textbox[name=q]"))[0]
        q.send_keys("[%s]" % tag)
        q.send_keys(Keys.RETURN)
        self.wait_for(15, lambda driver: self.driver.find_element_by_css_selector(QUESTION))
        self.model.questions = self.find_questions()

    def exit_(self):
        print("goodbye see you soon")
        try:
            self.driver.close()
        except:
            print("couldn't close driver, ignore if you closed webbrowser manually")
        sys.exit(123)

    def find_questions(self):
        return self._find_questions(self.driver.page_source)

    def _find_questions(self,html):
        soup = BeautifulSoup(html)
        questions = []
        for question_element in soup.select(QUESTION):
            question = self.create_question(question_element)
            questions.append(question)
        return questions

#new-post-activity

    def create_question(self, element:Tag) -> Question:
        id = element.attrs["id"]
        title_element = element.select(QUESTION_TITLE)[0]
        title = title_element.text
        link = WEBSITE + title_element.attrs["href"]
        user_name = element.select(USER_NAME)[0].text
        reputation_string = element.select(REPUTATION)[0].text.replace(",", "").replace("k", "000")
        reputation = float(reputation_string)
        tags = [i.text for i in element.select(TAG)]
        votes = int(element.select(VOTES)[0].text)
        answers = int(element.select(ANSWERS)[0].text)
        views = int(element.select(VIEWS)[0].text.replace("views", ""))
        time = element.select(TIME)[0].text

        user = User(user_name, reputation)
        return Question(id, title, user, link, votes, answers, views, tags, time)

    def wait_for(self, timeout, callback) -> WebElement:
        return WebDriverWait(self.driver, 15).until(callback)