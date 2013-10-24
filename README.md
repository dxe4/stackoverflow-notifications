=========
stackoverflow-notifications
=========

![notification!](https://raw.github.com/papaloizouc/stackoverflow-notifications/master/sonot.png "notification")

Under construction, will update the Readme when it's done.

Create notifications for new questions in a given tag.

I started this because stack overflow doesn't have any system tray notifications for new questions.

I believe it would be easier to just have a popup when a new question comes in the tag.


#Implementation

- selenium, phantomJS, beautiful soup 4, python3.3, PyQt4

- StackOverflow is using web socket to send real time updates.
- Use phnatomJS + selenium to login in stackoverflow
- Use beautiful soup to look for the "new questions" element
- if new questions are found, give a system notification
- Click on system tray to get the question link / more question info