from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtMaemo5 import *
import model
import view
import entry
import quicks
import editor
import sys

class Controller(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self._log = model.Timelog()

        self._window = view.MainWindow()
        self._window.show()

        self._lister = view.ListWindow(self._window)
        self._lister.hide()

        self._help = view.HelpWindow(self._window)
        self._help.hide()

        self.connect(self._window,
                     SIGNAL('pressed(QString)'),
                     self,
                     SLOT('_launch(QString)'))
        self.connect(self._window,
                     SIGNAL('edit(QString)'),
                     self,
                     SLOT('_edit(QString)'))
        self.connect(self._window,
                     SIGNAL('sync()'),
                     self,
                     SLOT('_sync()'))
        self.connect(self._window,
                     SIGNAL('showHelp()'),
                     self,
                     SLOT('_showHelp()'))

        self.connect(self._log,
                     SIGNAL("clear()"),
                     self._lister,
                     SLOT("clear()"))
        self.connect(self._log,
                     SIGNAL("found(int,QDateTime,QString)"),
                     self._lister,
                     SLOT("addRow(int,QDateTime,QString)"))

    def _launch(self, which):
        if which=='+':
           self._adder = entry.EntryWindow(-1, QDateTime.currentDateTime(), '')
           self._adder.show()
           self._adder.connect(self._adder,
                               SIGNAL('update(int,QDateTime,QString)'),
                               self,
                               SLOT('_update(int,QDateTime,QString)'))

           self._quicks = quicks.Quicks(self._adder)
           self._adder.connect(self._adder,
                               SIGNAL('showQuicks()'),
                               self._quicks,
                               SLOT('show()'))
           self.connect(self._quicks,
                        SIGNAL('selected(QString)'),
                        self._adder,
                        SLOT('setText(QString)'))
        elif which=='=':
            self._lister.show()
            self._log.load()

    def _update(self, place, datetime, message):
        self._log.save(place, datetime, message)
        self._info = QMaemo5InformationBox()
        self._info.information(self._window,
                               'Saved: '+message)

    def _edit(self, file):
        editor.edit(file)

    def _showHelp(self):
        self._help.show()

    def _sync(self):
        self._info = QMaemo5InformationBox()
        self._info.information(self._window,
                               'Git integration is not yet added.')

if __name__=='__main__':
    c = Controller(sys.argv)
    sys.exit(c.exec_())

