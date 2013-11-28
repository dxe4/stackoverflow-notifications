#!/usr/bin/env python3
from PyQt4 import QtGui
from PyQt4 import QtCore
import signal
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from bs4 import BeautifulSoup
from bs4.element import Tag

import time

from os.path import expanduser
import os
import configparser

from collections import OrderedDict

#TODO support multiple accounts in the future
#ACCOUNT_TYPES = ["stackexchange","google","yahoo","facebook","myopenid","livejournal","wordpress","blogger","verisign","claimid","aol"]

_browsers = {"firefox": webdriver.Firefox, "chrome": webdriver.Chrome, "opera": webdriver.Opera}
BROWSERS_LIST = sorted(_browsers.keys())
BROWSERS = OrderedDict(sorted(_browsers.items(), key=lambda t: t[0]))


def init_app() -> QtGui.QApplication:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QtGui.QFont("Monospace", 10))
    return app


class Model:
    def __init__(self):
        self.questions = []
        self.previous_questions = set()
        self.exception_timestamps = []
        self.userName = None
        self.password = None
        self.tag = None
        self.browser = None

    def is_exception_overflow(self):
        self.exception_timestamps.append(int(time.time()))
        if len(self.exception_timestamps) > 10:
            last = self.exception_timestamps[-1:]
            new_list = list(filter(lambda i: i == last, self.exception_timestamps[-10:]))
            if len(new_list) < 2:
                return True
        return False

    def update_questions(self, questions):
        self.previous_questions = self.previous_questions.union(self.questions)
        self.questions = [i for i in questions if i not in self.previous_questions]
        self.previous_questions = self.previous_questions.union(self.questions)


class Question:
    def __init__(self, id, title, user, link, votes, answers, views, tags, time):
        self.id = id
        self.user = user
        self.title = title
        self.link = link
        self.votes = votes
        self.answers = answers
        self.views = views
        self.tags = tags
        self.time = time

    def __str__(self):
        return str(vars(self))

    def __eq__(self, other):
        return self.link == other.link

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.link)


class User:
    def __init__(self, name, reputation):
        self.name = name
        self.reputation = reputation

    def __str__(self):
        return str(vars(self))


class Scrapper():
    QUESTION = "[id^=question-summary-]"
    QUESTION_TITLE = ".question-hyperlink"
    USER_NAME = ".user-details [href^=/users/]"
    REPUTATION = ".reputation-score"
    TAG = ".post-tag"
    VOTES = ".vote-count-post strong"
    ANSWERS = ".status strong"
    VIEWS = ".views"
    WEBSITE = "http://stackoverflow.com/"
    TIME = ".relativetime"
    NEW_QUESTION = ".new-post-activity"


    def __init__(self, model):
        self.driver = BROWSERS[model.browser]()
        self.model = model

    def login(self, email:str, password:str):
        print("logging in.... %s " % (email))
        self.driver.get(Scrapper.WEBSITE + "users/login#log-in")
        if self.driver.current_url != Scrapper.WEBSITE:
            self._login(email, password)
        del self.model.password

    def _login(self, email:str, password:str):
        frame = self.wait_for(15, lambda driver: driver.find_element_by_id(
            "affiliate-signin-iframe"))#if allready logged in need to skip
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
        self.wait_for(15, lambda driver: self.driver.find_element_by_css_selector(Scrapper.QUESTION))
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

    def _find_questions(self, html):
        soup = BeautifulSoup(html)
        questions = []
        for question_element in soup.select(Scrapper.QUESTION):
            question = self.create_question(question_element)
            questions.append(question)
        return questions

    def create_question(self, element:Tag) -> Question:
        id = element.attrs["id"]
        title_element = element.select(Scrapper.QUESTION_TITLE)[0]
        title = title_element.text
        link = Scrapper.WEBSITE + title_element.attrs["href"]
        user_name = element.select(Scrapper.USER_NAME)[0].text
        reputation_string = element.select(Scrapper.REPUTATION)[0].text.replace(",", "").replace("k", "000")
        reputation = float(reputation_string)
        tags = [i.text for i in element.select(Scrapper.TAG)]
        votes = int(element.select(Scrapper.VOTES)[0].text)
        answers = int(element.select(Scrapper.ANSWERS)[0].text)
        views = int(element.select(Scrapper.VIEWS)[0].text.replace("views", ""))
        time = element.select(Scrapper.TIME)[0].text

        user = User(user_name, reputation)
        return Question(id, title, user, link, votes, answers, views, tags, time)

    def wait_for(self, timeout, callback) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(callback)

    def wait_for_questions(self, ui_signal):
        while True:
            try:
                element = self.wait_for(200, lambda driver: driver.find_elements_by_css_selector(Scrapper.NEW_QUESTION))
            except Exception as e:#not important no new questions found timeout...
                print(e)
                if self.model.is_exception_overflow():
                    print("Exception overflow, exiting... Something is wrong with the browser...")
                    self.exit_()
                element = None
            if element:
                element[0].click()
                self.model.update_questions(self.find_questions())
                ui_signal.emit(self.model.questions)


class UIThread(QtCore.QThread):
    ui_signal = QtCore.pyqtSignal(list)

    def __init__(self, scrapper, model):
        QtCore.QThread.__init__(self)
        self.scrapper = scrapper
        self.model = model


    #TODO deal with exception in another thread. also must exit selenoium webdriver if process is killed.
    def run_scrapper(self, scrapper:Scrapper, model:Model):
        scrapper.model = model
        scrapper.login(model.userName, model.password)
        scrapper.search_tag(model.tag)
        scrapper.wait_for_questions(self.ui_signal)

    def run(self):
        self.run_scrapper(self.scrapper, self.model)


class View:
    def __init__(self, model:Model):
        self.model = model
        self.scrapper = Scrapper(self.model)
        self.widget = QtGui.QWidget()
        self.trayIcon = SystemTrayIcon(QtGui.QIcon("stackoverflow_logo.png"), self.widget)
        self.trayIcon.show()
        self.thread = UIThread(self.scrapper, self.model)
        self.thread.ui_signal.connect(self.show_questions)
        self.thread.start()
        self.register_exit_callback(self.scrapper.exit_)


    def register_exit_callback(self, exit_callback):
        self.trayIcon.register_exit_callback(exit_callback)

    def show_questions(self, questions:list):
        build_string = "\n\n".join([i.title[:50] for i in questions])
        self.trayIcon.showMessage("%s New Questions" % len(questions), build_string, QtGui.QSystemTrayIcon.NoIcon)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.dialog = None
        self.menu = QtGui.QMenu(parent)

    def register_exit_callback(self, exit_callback):
        #self.activated.connect(self.onClicked)
        self.setContextMenu(self.menu)
        self.exitAction = self.menu.addAction("Exit")
        QtCore.QObject.connect(self.exitAction, QtCore.SIGNAL('triggered()'), exit_callback)


    def onClicked(self, *args, **kwargs):
        if args[0] == 1: #right click is for menu
            return

        if hasattr(self, "dialog") and self.dialog: #hide if all-ready exists
            del self.dialog
            return


class Login(QtGui.QDialog):
    def __init__(self, model:Model):
        QtGui.QDialog.__init__(self)
        self.model = model
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.checkBox = QtGui.QCheckBox("")
        self.tag = QtGui.QLineEdit("")
        self.browsers = QtGui.QComboBox(self)
        for browser in BROWSERS.keys(): self.browsers.addItem(browser)

        layout = QtGui.QFormLayout(self)
        layout.addRow("Username", self.textName)
        layout.addRow("Password", self.textPass)
        layout.addRow("Browser", self.browsers)
        layout.addRow("Tag", self.tag)
        layout.addRow("Remember\n(won't save password)", self.checkBox)
        layout.addRow("", self.buttonLogin)

        settings = self.read_settings()
        self.init_settings(settings)

    def init_settings(self, settings:dict):
        if not settings:
            return

        def setup(func:callable, key:str):
            if key and key in settings: func(settings[key])

        setup(self.textName.setText, "username")
        setup(self.tag.setText, "tag")
        self.checkBox.setChecked(True)
        if "browser" in settings:
            self.browsers.setCurrentIndex(BROWSERS_LIST.index(settings["browser"]))

    def handleLogin(self):
        if self.textPass.text() and self.textPass.text() and self.tag.text():
            self.accept()
            self.model.userName = self.textName.text()
            self.model.password = self.textPass.text()
            self.model.tag = self.tag.text()
            self.model.browser = str(self.browsers.currentText())
            if self.checkBox.isChecked():
                self.memorize()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')

    def memorize(self):
        with open(os.path.join(expanduser("~"), ".sonot_settings"), "w") as f:
            print("[Settings]", file=f)
            print("username: %s" % self.model.userName, file=f)
            print("remember: True", file=f)
            print("tag: %s" % self.tag.text(), file=f)
            print("browser: %s" % str(self.browsers.currentText()), file=f)

    def read_settings(self):
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read(os.path.join(expanduser("~"), ".sonot_settings"))
            return {i: config_parser.get("Settings", i) for i in config_parser.options("Settings")}
        except:#no config file
            pass

def run():
    app = init_app()
    model = Model()
    if Login(model).exec_() != QtGui.QDialog.Accepted:
        sys.exit(0)
    view = View(model)
    view.scrapper.exit_(app.exec_())

if __name__ == '__main__':
    run()