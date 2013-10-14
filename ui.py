import sys
from PyQt4 import QtGui
import signal
import time


def doSomething():
    sys.exit(666)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.dialog = None

        self.menu = QtGui.QMenu(parent)

        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(doSomething)
        self.activated.connect(self.clicked)
        self.setContextMenu(self.menu)

    def clicked(self, *args, **kwargs):
        if args[0] == 1:#right click
            return
        if self.dialog is not None:#hide if all-ready exists
            self.dialog = None
            return
        self.dialog = QtGui.QDialog()
        self.dialog.setWindowTitle("Title")
        self.dialog.show()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    widget = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("stackoverflow_logo.png"), widget)
    trayIcon.show()
    time.sleep(1)
    trayIcon.showMessage("Foo!!!", "Bar!!!", QtGui.QSystemTrayIcon.NoIcon)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
