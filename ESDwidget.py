from PyQt6 import QtWidgets, QtCore
from Store import Store
from ESDAction import Action
import sys

class ESD(QtWidgets.QWidget):
    def __init__(self, id: str):
        super().__init__()
        self.id = id
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: #c0c0c0;
                border: 2px solid #df23df;
                border-radius: 0px;
            }
        """)
        
        self._Initui()
    def _Initui(self):
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.name = QtWidgets.QLabel(self.id)
        self.vlayout.addWidget(self.name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vlayout)

def window():
    app = QtWidgets.QApplication([])
    window = ESD("0ESD021")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
