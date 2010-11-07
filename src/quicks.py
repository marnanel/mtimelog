from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtMaemo5 import *
import sys
import model

class Quicks(QObject):
   def __init__(self, parent):
      QObject.__init__(self)
      self._parent = parent

   def show(self):
      quicks = model.Quicks()

      self._model = QStringListModel(quicks.contents())
      self._pick = QMaemo5ListPickSelector()
      self._pick.setModel(self._model)
      self.connect(self._pick,
                   SIGNAL("selected(QString)"),
                   self,
                   SIGNAL("selected(QString)"))

      widget = self._pick.widget(self._parent)
      widget.setWindowTitle('Quick choices')
      widget.show()

