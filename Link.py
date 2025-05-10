from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, pyqtSignal
import sys


class Link(QtWidgets.QWidget):
    changePageSignal = pyqtSignal(int)

    def __init__(self,dest):
        super().__init__()
        self.dest = dest
        # self.distination = distination
        self.InitUi()

    def InitUi(self):
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        # self.setGeometry(99,99,1000,1000)
        self.setWindowOpacity(0.5)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.changePageSignal.emit(self.dest)
    
    def Updatingvalue(self,data):
        self.value = data.get(self.value)
        self.update()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Link()
    widget.show()
    sys.exit(app.exec())