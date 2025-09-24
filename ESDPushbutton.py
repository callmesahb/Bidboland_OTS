from PyQt6 import QtWidgets,QtGui,QtCore
from Store import Store
import sys

class Button(QtWidgets.QWidget):
    buttontriggered = QtCore.pyqtSignal(str)
    def __init__(self,id,store:Store):
        super().__init__()
        # self.setFixedSize(250,50)
        self.setStyleSheet("background-color:black")
        self.id = id
        self.store = store
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self._InitUI()
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.SetTexting()
    def SetTexting(self):
        self.permission = QtWidgets.QPushButton("OFF",self)
        self.permission.setStyleSheet("color:white")
        self.permission.clicked.connect(self.pressbtn1)
        self.vlayout.addWidget(self.permission)
        self.setLayout(self.vlayout)
    
    
    
    
    def pressbtn1(self):
        if self.permission.text() == "OFF":
            self.store.settingValueOPC("1PB002L",2)
            self.permission.setText("ON")
            self.store.settingValueOPC("1PB003L",2)
            self.buttontriggered.emit(self.permission.text())
        elif self.permission.text() == "ON":
            self.store.settingValueOPC("1PB002L",1)
            self.store.settingValueOPC("1PB003L",1)
            self.permission.setText("OFF")
            self.buttontriggered.emit(self.permission.text())
    def pressbtn(self):
        varid = self.id + "L"
        valuepb02 = self.store.finaltag["1PB002L"]
        if valuepb02 == 1:
            self.store.settingValueOPC("1PB002L",1)
            self.permission.setText("OFF")
        elif self.permission.text() == "ON":
            self.store.settingValueOPC("1PB002L",2)
        self.buttontriggered.emit(self.permission.text())
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Button()
    window.show()
    app.exec()