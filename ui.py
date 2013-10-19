__author__ = 'papaloizouc'

import sys
from PyQt4 import QtGui, QtCore
import signal
import time
from model import Model

signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QtGui.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
app.setFont(QtGui.QFont("Monospace", 13))
global _model

class View:
    def __init__(self, exit_callback, model:Model):
        _model = model
        widget = QtGui.QWidget()
        trayIcon = SystemTrayIcon(QtGui.QIcon("stackoverflow_logo.png"), widget, exit_callback=exit_callback)
        trayIcon.show()
        time.sleep(1)
        trayIcon.showMessage("New Questions !!!", "Question 1", QtGui.QSystemTrayIcon.NoIcon)
        exit_callback(app.exec_())


class Dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("New Questions")
        self.list_view = ListView()

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.qlist)
        self.setLayout(hbox)


    def add_questions(self,questions):
        self.list_view.clear()
        for question in self.questions:
            self.list_view.addItem(QuestionView(question))


class ListView(QtGui.QWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

    def addItem(self,item):
        self.layout.addWidget(item)

    def clear(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)



class QuestionView(QtGui.QWidget):
    def __init__(self,question):
        QtGui.QWidget.__init__(self)
        self.add()

    def add(self):

        hbox = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()
        vbox2 = QtGui.QVBoxLayout()
        vbox3 = QtGui.QVBoxLayout()

        hbox.addWidget(QtGui.QLabel("test            -"))

        vbox2.addWidget(QtGui.QLabel("testv1"))
        vbox2.addWidget(QtGui.QLabel("testv"))

        vbox3.addWidget(QtGui.QLabel("testv1"))
        vbox3.addWidget(QtGui.QLabel("testv"))

        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)

        hbox.addLayout(hbox2)
        self.setLayout(hbox)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None, exit_callback=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.dialog = None
        self.menu = QtGui.QMenu(parent)

        self.exitAction = self.menu.addAction("Exit")

        QtCore.QObject.connect(self.exitAction, QtCore.SIGNAL('triggered()'), exit_callback)
        QtCore.QObject.connect(self, QtCore.SIGNAL('activated()'), self.clicked)

        self.setContextMenu(self.menu)

    def clicked(self, *args, **kwargs):
        if args[0] == 1:#right click is for menu
            return

        if self.dialog is not None:#hide if all-ready exists
            self.dialog = None
            return

        self.dialog = Dialog()
        self.dialog.show()