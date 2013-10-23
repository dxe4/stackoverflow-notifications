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


EMAIL = ""
PASSWORD = ""

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
NEW_QUESTION = ".new-post-activity"


def init_app() -> QtGui.QApplication:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QtGui.QFont("Monospace", 10))
    return app


class Model:
    def __init__(self):
        self.questions = []


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


class User:
    def __init__(self, name, reputation):
        self.name = name
        self.reputation = reputation

    def __str__(self):
        return str(vars(self))


class Scrapper():
    def __init__(self, model):
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

    def _find_questions(self, html):
        soup = BeautifulSoup(html)
        questions = []
        for question_element in soup.select(QUESTION):
            question = self.create_question(question_element)
            questions.append(question)
        return questions

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
        return WebDriverWait(self.driver, timeout).until(callback)

    def wait_for_questions(self, ui_signal):
        while True:
            try:
                element = self.wait_for(200, lambda driver: driver.find_elements_by_css_selector(NEW_QUESTION))
            except Exception as e:#not important no new questions found...
                print("error" + e)
                element = None
            if element:
                element[0].click()
                ui_signal.emit(self.find_questions())


class UIThread(QtCore.QThread):
    ui_signal = QtCore.pyqtSignal(list)

    def __init__(self, scrapper, model):
        QtCore.QThread.__init__(self)
        self.scrapper = scrapper
        self.model = model


    #TODO deal with exception in another thread. also must exit selenoium webdriver if process is killed.
    def run_scrapper(self, scrapper:Scrapper, model:Model):
        scrapper.model = model
        scrapper.login(EMAIL, PASSWORD)
        scrapper.search_tag("java")
        scrapper.wait_for_questions(self.ui_signal)

    def run(self):
        self.run_scrapper(self.scrapper, self.model)


class View:
    def __init__(self):
        self.model = Model()
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
        pass


    def onClicked(self, *args, **kwargs):
        if args[0] == 1: #right click is for menu
            return

        if hasattr(self, "dialog") and self.dialog: #hide if all-ready exists
            del self.dialog
            return


if __name__ == '__main__':
    app = init_app()
    view = View()
    view.scrapper.exit_(app.exec_())


