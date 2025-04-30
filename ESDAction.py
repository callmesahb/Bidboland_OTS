from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, pyqtSignal
from Store import Store
import sys


class Action(QtWidgets.QWidget):

    def __init__(self,action:list,store:Store):
        super().__init__()
        self.resize(200, 200)
        self.color = "#000"
        self.action = action
        self.store = store
        self.InitUi()

    def InitUi(self):
        self.setWindowOpacity(1)

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
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Action()
    widget.show()
    sys.exit(app.exec())