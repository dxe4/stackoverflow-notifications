=========
stackoverflow-notifications
=========

![login!](https://raw.github.com/papaloizouc/stackoverflow-notifications/master/doc/login.png "login")
![notification!](https://raw.github.com/papaloizouc/stackoverflow-notifications/master/doc/sonot.png "notification")

ALPHA

Create notifications for new questions in a given tag.

I started this because stack overflow doesn't have any system tray notifications for new questions.

I believe it would be easier to just have a popup when a new question comes in the tag.


#Install
(it works for me but if you have a problem let me know):


**Requires** (I tried to automate it with sh files) :
- Python3 (i used 3.3)
- PyQt4
- selenium
- BeautifulSoup4


Linux:
---

    sudo bash ubuntu.sh

    sudo bash arch.sh

    sonot


Linux(other):
---

    install python3.3, python3-pyqt4, python3-pip

    pip-3.3 install selenium,BeautifulSoup4

    python sonot.py

    You may as well copy it in /opt and and a shortcut in /bin

Mac
---

    It should be something similar with Linux(other) section, any help to automate is appreciated.


Windows
---

    The only way i know of installing PyQt on windows is to click next all the time...