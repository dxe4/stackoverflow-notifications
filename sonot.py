from scrapper import Scrapper
import ui
from model import Model
from PyQt4 import QtGui
import signal
import sys

EMAIL = ""
PASSWORD = ""



#TODO deal with exception in another thread. also must exit selenoium webdriver if process is killed.
def run_scrapper(scrapper:Scrapper, model:Model):
    scrapper.model = model
    scrapper.login(EMAIL, PASSWORD)
    scrapper.search_tag("python")

def init_app() -> QtGui.QApplication:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QtGui.QFont("Monospace", 10))
    return app

if __name__ == '__main__':
    app = init_app()
    model_ = Model()
    view = ui.View(model_)
    scrapper = Scrapper(model_, view)
    view.register_exit_callback(scrapper.exit_)
    run_scrapper(scrapper, model_)
    scrapper.exit_(app.exec_())

