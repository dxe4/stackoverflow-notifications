from scrapper import Scrapper
import ui
from model import Model
from model import Question,User
from PyQt4 import QtGui
import signal
import sys
import threading

EMAIL = ""
PASSWORD = ""



def run_scrapper(scrapper:Scrapper, model:Model):
    #scrapper.model = model
    #scrapper.login(EMAIL, PASSWORD)
    #scrapper.search_tag("python")
    temp = [{'title': 'python getting a list from', 'time': '11 mins ago', 'views': 23, 'answers': 2,
          'tags': ['python', 'python-3.x'], 'user': {'reputation': 51.0, 'name': 'Michael C'}, 'votes': 0,
          'id': 'question-summary-19472748',
          'link': 'http://www.stackoverflow.com/questions/19472748/python-getting-a-list-from'},
         {'title': 'Text is replaced at end of file?', 'time': '13 mins ago', 'views': 11, 'answers': 0,
          'tags': ['python', 'string', 'file', 'replace'], 'user': {'reputation': 48.0, 'name': 'user1871869'},
          'votes': 0, 'id': 'question-summary-19472723',
          'link': 'http://www.stackoverflow.com/questions/19472723/text-is-replaced-at-end-of-file'}, {
         'title': 'how to improve so that the output plot is changed as I move my slider(a parameter of function) in a GUI program of python?',
         'time': '16 mins ago', 'views': 3, 'answers': 0,
         'tags': ['python', 'user-interface', 'matplotlib', 'scipy', 'signals'],
         'user': {'reputation': 8.0, 'name': 'Guangyue He'}, 'votes': 0, 'id': 'question-summary-19472706',
         'link': 'http://www.stackoverflow.com/questions/19472706/how-to-improve-so-that-the-output-plot-is-changed-as-i-move-my-slidera-paramete'}
        ]
    temp2 = []
    for i in temp:
        q = Question(i["id"],i["title"], User(i["user"]["name"],i["user"]["reputation"]),i["link"],i["votes"],i["answers"],i["views"],i["tags"],i["time"])
        temp2.append(q)
    model.questions = temp2[:4]


def init_app() -> QtGui.QApplication:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QtGui.QFont("Monospace", 12))
    return app


if __name__ == '__main__':
    app = init_app()

    model_ = Model()
    view = ui.View(model_)
    scrapper = Scrapper(model_, view)
    view.register_exit_callback(scrapper.exit_)

    thread = threading.Thread(target=run_scrapper, args=(scrapper, model_))
    thread.daemon = True
    thread.start()

    scrapper.exit_(app.exec_())

