from scrapper import Scrapper
import ui
from model import Model

from PyQt4 import QtGui
import signal
import sys
import threading

EMAIL = ""
PASSWORD = ""


def run_scrapper(scrapper:Scrapper,model:Model):
    scrapper.model = model
    scrapper.login(EMAIL, PASSWORD)
    scrapper.search_tag("python")


def init_app() -> QtGui.QApplication:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QtGui.QFont("Monospace", 13))
    return app


if __name__ == '__main__':
    app = init_app()

    model = Model()
    scrapper = Scrapper()
    view = ui.View(scrapper.exit_, model)

    thread = threading.Thread(target=run_scrapper, args=(scrapper,model))
    thread.daemon = True
    thread.start()

    scrapper.exit_(app.exec_())

