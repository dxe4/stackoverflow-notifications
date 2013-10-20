__author__ = 'papaloizouc'

import time
from PyQt4 import QtGui, QtCore
from model import Model


class View:
    def __init__(self,model:Model):
        global _model
        _model = model
        self.widget = QtGui.QWidget()
        self.trayIcon = SystemTrayIcon(QtGui.QIcon("stackoverflow_logo.png"), self.widget)
        self.trayIcon.show()
        time.sleep(1)
        self.trayIcon.showMessage("New Questions !!!", "Question 1", QtGui.QSystemTrayIcon.NoIcon)

    def register_exit_callback(self,exit_callback):
        self.trayIcon.register_exit_callback(exit_callback)

class Dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("New Questions")
        self.list_view = ListView()

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.list_view)
        self.setLayout(hbox)


    def add_questions(self,questions):
        for question in questions:
            self.list_view.addItem(QuestionView(question))


class ListView(QtGui.QWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

    def addItem(self,item):
        self.layout.addWidget(item)


class QuestionView(QtGui.QWidget):
    def __init__(self,question):
        QtGui.QWidget.__init__(self)
        self.add()

    def add(self):
        hbox = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()

        hbox.addWidget(QtGui.QLabel("test            -"))
        hbox2.addWidget(QtGui.QLabel("testv1"))
        hbox2.addWidget(QtGui.QLabel("testv"))
        hbox2.addWidget(QtGui.QLabel("testv1"))
        hbox2.addWidget(QtGui.QLabel("testv"))

        hbox.addLayout(hbox2)
        self.setLayout(hbox)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.dialog = None
        self.menu = QtGui.QMenu(parent)

    def register_exit_callback(self,exit_callback):
        self.activated.connect(self.onClicked)
        self.setContextMenu(self.menu)
        self.exitAction = self.menu.addAction("Exit")
        QtCore.QObject.connect(self.exitAction, QtCore.SIGNAL('triggered()'), exit_callback)
        pass


    def onClicked(self, *args, **kwargs):
        if args[0] == 1: #right click is for menu
            return

        if hasattr(self,"dialog")  and self.dialog: #hide if all-ready exists
            del self.dialog
            return

        self.dialog = Dialog()
        self.dialog.add_questions(_model.questions)
        self.dialog.show()