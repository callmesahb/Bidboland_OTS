from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, pyqtSignal
from Store import Store
from Store import Store
import sys


class TextAction(QtWidgets.QWidget):

    def __init__(self,text,variableid,store:Store):
        super().__init__()
        self.resize(200, 200)
        self.color = "#fff"
        self.text = text
        self.variableid = variableid
        self.store = store
        self.setStyleSheet("background-color:#666666")
        self.label = QtWidgets.QLabel("",self)
        self.InitUi()

    def InitUi(self):
        self.setWindowOpacity(1)
        self.vlayout = QtWidgets.QVBoxLayout()
        
        self.label.setText(self.text)
        self.label.setStyleSheet("color:#fff")
        self.vlayout.addWidget(self.label)
        self.setLayout(self.vlayout)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            print("SALAM")
            
    def Updatingvalue(self,data):
        self.value = data.get(self.value)
        self.update()
        
    def doaction(self):
        tag = self.action[0]
        action = self.action[1]
        if action == "shutdown" or action == "close":
            self.store.opc.setValue(tag,2)
        else:
            pass
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(self.color), 3))
        painter.drawRect(self.rect())
    
    @QtCore.pyqtSlot()
    def updatevalue(self):
        value = self.store.finaltag[self.variableid]
        if value == 2:
            print(value)
            self.label.setStyleSheet("color:red;")
            self.color = "red"
            print(value)
        # print(value)
        else:
            self.label.setStyleSheet("color:#fff;")
            self.color = "#fff"
            print(value)