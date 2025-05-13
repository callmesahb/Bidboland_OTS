from PyQt6 import QtWidgets, QtCore,QtGui
from Store import Store
from ESDAction import Action
import sys

class ESD(QtWidgets.QWidget):
    changepagebyesd = QtCore.pyqtSignal(int)
    def __init__(self, id: str,dest):
        super().__init__()
        self.id = id
        self.dest = dest
        # self.setFixedSize(140,80)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: #c0c0c0;
                border: 2px solid #0000ff;
                border-radius: 0px;
            }
        """)
        
        self._Initui()
    def _Initui(self):
        self.vlayout = QtWidgets.QVBoxLayout(self)
        texting = "   " + self.id
        self.name = QtWidgets.QLabel(self.id)
        self.vlayout.addWidget(self.name, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.vlayout)
        
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            print("SALAM")
            self.changepagebyesd.emit(self.dest)
            print(f"{self.dest} is emitted")
            
def window():
    app = QtWidgets.QApplication([])
    window = ESD("0ESD021")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
