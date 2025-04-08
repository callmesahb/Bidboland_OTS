from PyQt6 import QtWidgets,QtCore,QtGui
from HandSwitch import HandSwitch
import sys

class Equipment(QtWidgets.QWidget):
    def __init__(self,name,type,btns):
        super().__init__()
        self.type = type
        self.name = name
        self.btns = btns
        self.setWindowOpacity(0)
        
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.type == "handswitch":
                self.hs = HandSwitch(self.name,self.btns)
                self.hs.show()