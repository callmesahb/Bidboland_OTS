from PyQt6 import QtWidgets, QtCore
from Store import Store
from ESDAction import Action
import sys

class PSTWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: #676767;
                border: 2px solid #000;
                border-radius: 3px;
            }
        """)
        # print("PST added")
        self._Initui()
        
    def _Initui(self):
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.settingname()
    
    def settingname(self):
        self.text = QtWidgets.QLabel("PST",self)
        self.text.setStyleSheet("color:black;font-size:14px")
        self.mainlayout.addWidget(self.text,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        
        
        
def window():
    app = QtWidgets.QApplication([])
    window = PSTWidget()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
