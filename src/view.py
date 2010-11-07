from PySide.QtCore import *
from PySide.QtGui import *
import sys

class MainButton(QPushButton):
    def __init__(self, symbol):
        QPushButton.__init__(self)

        self.setText(symbol)
        self.setFont(QFont("Helvetica",
                           30))
        self._symbol = symbol

        self.connect(self,
                     SIGNAL('pressed()'),
                     self,
                     SLOT('_sendPush()'))

    def _sendPush(self):
        self.emit(SIGNAL('pressed(QString)'),
                  self._symbol)

class EditAction(QAction):
    def __init__(self, parent, message, filename):
        QAction.__init__(self, message, parent)
        self.connect(self, SIGNAL("triggered()"),
                     self, SLOT("_sendFilename()"))
        self._filename = filename

    def _sendFilename(self):
        self.emit(SIGNAL("edit(QString)"),
                  self._filename)



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle('mtimelog')
        self.setAttribute(Qt.WA_Maemo5StackedWindow)

        self._widget = QWidget()
        self.setCentralWidget(self._widget)

        self._layout = QHBoxLayout()
        self._widget.setLayout(self._layout)

        for symbol in ('=', '+'):
            button = MainButton(symbol)
            button.connect(button,
                           SIGNAL('pressed(QString)'),
                           self,
                           SIGNAL('pressed(QString)'))
            self._layout.addWidget(button)

        for editing in (['Edit timelog', '/home/user/.gtimelog/mtimelog.txt'],
                        ['Edit quicks', '/home/user/.gtimelog/quicks.txt']):
            action = EditAction(self, editing[0], editing[1])
            action.connect(action, SIGNAL('edit(QString)'),
                           self, SIGNAL('edit(QString)'))
            self.menuBar().addAction(action)

        sync = QAction('Sync', self)
        self.connect(sync, SIGNAL('triggered()'),
                     self, SIGNAL('sync()'))
        self.menuBar().addAction(sync)

        about = QAction('Help', self)
        self.connect(about, SIGNAL('triggered()'),
                     self, SIGNAL('showHelp()'))
        self.menuBar().addAction(about)

class ListWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('Entries')
        self.setAttribute(Qt.WA_Maemo5StackedWindow)

        self._model = QStandardItemModel()

        self._listview = QListView()
        self.setCentralWidget(self._listview)
        self._listview.setModel(self._model)

    def clear(self):
        self._model.clear()

    def addRow(self, place, datetime, message):
        line = datetime.toString() + ': '
        line = line + message
        qsi = QStandardItem(line)
        self._model.appendRow(qsi)
        self._listview.scrollToBottom()

class HelpWindow(QMainWindow):
   def __init__(self, parent):
      QMainWindow.__init__(self, parent)
      self.setWindowTitle('mtimelog help')
      self.setAttribute(Qt.WA_Maemo5StackedWindow)

      help = QTextEdit()

      try:
         content = file('/opt/mtimelog/help.html').read()
         help.setText(content)
      except:
         help.setText('Could not open the help.')

      help.setReadOnly(True)

      self.setCentralWidget(help)
