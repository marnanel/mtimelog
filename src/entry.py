from PySide.QtCore import *
from PySide.QtGui import *
import sys
import time

class EntryWindow(QDialog):

    _timeFormat = '%Y-%m-%d %H:%M'

    def __init__(self, place, datetime, message):
        QDialog.__init__(self)

        self.connect(self,
                     SIGNAL('finished(int)'),
                     self,
                     SLOT('_sendResult()'))

        self._place = place
        self._datetime = datetime

        if place==-1:
          self.setWindowTitle('Add entry')
        else:
          self.setWindowTitle('Edit entry')

        self.m_layout = QVBoxLayout()
        self.setLayout(self.m_layout)

        self.m_date = QLabel(time.strftime(self._timeFormat,
                                           time.localtime(datetime.toTime_t())))

        self.m_date.setAlignment(Qt.AlignHCenter|
                                 Qt.AlignVCenter)
        self.m_layout.addWidget(self.m_date)

        self.m_entry = QTextEdit()
        self.m_entry.setText(message)
        self.m_layout.addWidget(self.m_entry)

        self.m_buttonBox = QWidget()
        self.m_layout.addWidget(self.m_buttonBox)

        self.m_buttonLayout = QHBoxLayout()
        self.m_buttonBox.setLayout(self.m_buttonLayout)

        if place==-1:
           slacking = 1
        else:
           if message.endswith(' **'):
              slacking = 1
              message = message[:-3]
           else:
              slacking = 0

        self.m_slack = QPushButton("Slack")
        self.m_slack.setCheckable(True)
        self.m_slack.setChecked(slacking)
        self.m_slack.connect(self.m_slack,
                            SIGNAL("pressed()"),
                            self,
                            SLOT("_pressedSlack()"))
        self.m_buttonLayout.addWidget(self.m_slack)

        self.m_work = QPushButton("Work")
        self.m_work.setCheckable(True)
        self.m_work.setChecked(not slacking)
        self.m_work.connect(self.m_work,
                            SIGNAL("pressed()"),
                            self,
                            SLOT("_pressedWork()"))
        self.m_buttonLayout.addWidget(self.m_work)

        self.m_choices = QPushButton("...")
        self.m_buttonLayout.addWidget(self.m_choices)
        self.m_choices.connect(self.m_choices,
                               SIGNAL('pressed()'),
                               self,
                               SIGNAL('showQuicks()'))

    def setText(self, message):
        if message.endswith(' **'):
           message = message[:-3]
           slack = True
        else:
           slack = False
        self.m_work.setChecked(not slack)
        self.m_slack.setChecked(slack)
        self.m_entry.setText(message)

    def _pressedSlack(self):
        self.m_work.setChecked(self.m_slack.isChecked())

    def _pressedWork(self):
        self.m_slack.setChecked(self.m_work.isChecked())

    def _sendResult(self):
        message = self.m_entry.toPlainText()

        if message=='':
           return

        if self.m_slack.isChecked():
           message += ' **'

        self.emit(SIGNAL('update(int, QDateTime, QString)'),
                  self._place,
                  self._datetime,
                  message)
