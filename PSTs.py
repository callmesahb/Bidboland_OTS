from PyQt6 import QtWidgets, QtCore
from Store import Store
from ESDAction import Action
import sys

class PSTWidget(QtWidgets.QWidget):
    def __init__(self,variableid:list,store):
        super().__init__()
        self.variableid = variableid
        self.store = store
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: #676767;
                border: 2px solid #ffffff;
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
        self.text.setStyleSheet("color:#ffffff;font-size:14px")
        self.mainlayout.addWidget(self.text,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        
    def readingvalue(self):
        value = self.store.finaltag[self.variableid[0]]
        rrvar = self.variableid[0].replace("LG","")
        if value == 2:
            self.store.settingValueOPC(rrvar,2)
            self.text.setStyleSheet("color:#ff0000;font-size:14px")
            self.setStyleSheet("""
                QWidget {
                    background: #676767;
                    border: 2px solid #ff0000;
                    border-radius: 3px;
                }
            """)
        else:
            self.text.setStyleSheet("color:#ffffff;font-size:14px")
            self.setStyleSheet("""
                QWidget {
                    background: #676767;
                    border: 2px solid #ffffff;
                    border-radius: 3px;
                }
            """)
        
        
def window():
    app = QtWidgets.QApplication([])
    window = PSTWidget()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
