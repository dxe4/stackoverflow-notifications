__author__ = 'papaloizouc'

import sys
from PyQt4 import QtGui, QtCore
import signal
import time


class View:
    def __init__(self, exit_callback):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QtGui.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        widget = QtGui.QWidget()
        trayIcon = SystemTrayIcon(QtGui.QIcon("stackoverflow_logo.png"), widget,exit_callback=exit_callback)
        trayIcon.show()
        time.sleep(1)
        trayIcon.showMessage("New Questions !!!", "Question 1", QtGui.QSystemTrayIcon.NoIcon)
        exit_callback(app.exec_())


class Dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("New Questions")

        self.qlist = QtGui.QListWidget()

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.qlist)
        self.setLayout(hbox)
        self.questions = []

    def add_questions(self, questions):
        self.questions = questions
        self._add_questions()

    def _add_questions(self):
        self.qlist.clear()
        for question in self.questions:
            self.qlist.addItem(question)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None,exit_callback=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.dialog = None
        self.menu = QtGui.QMenu(parent)

        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(exit_callback)
        self.activated.connect(self.clicked)
        self.setContextMenu(self.menu)

    def clicked(self, *args, **kwargs):
        if args[0] == 1:#right click is for menu
            return

        if self.dialog is not None:#hide if all-ready exists
            self.dialog = None
            return

        self.dialog = Dialog()
        self.dialog.add_questions(["Question 1", "Question 2"])
        self.dialog.show()
