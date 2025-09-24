from PyQt6 import QtWidgets, QtCore,QtGui
from Store import Store
from ESDAction import Action
from Store import Store
import sys

class ESD(QtWidgets.QWidget):
    changepagebyesd = QtCore.pyqtSignal(int)
    def __init__(self, id: str,dest,store:Store):
        super().__init__()
        self.id = id
        self.dest = dest
        self.store = store
        # self.setFixedSize(140,80)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background: #c0c0c0;
                border: 2px solid #0000ff;
                border-radius: 0px;
            }
        """)
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.checkingvalue)
        # self.timer.start(2000)
        self.names = ["1ESD3908","1ESD3217","1ESD3219","1ESD3326","1ESD3323","1ESD3906","1ESD3905","1ESD3907","1ESD3314","1ESD3315","1ESD3316A","1ESD3316B","1ESD3316C","1ESD3316D","1ESD3321","1ESD3307","1ESD3322","1ESD3325"]
        
        self._Initui()
    # def checkingvalue(self):
    #     for name in self.names:
    #         value = self.store.finaltag[name]
    #         if value == 1:
    #             nameid = name + "L"
    #             self.store.settingValueOPC(nameid,1)
    #         elif value == 2:
    #             nameid = name + "L"
    #             self.store.settingValueOPC(nameid,2)
    def _Initui(self):
        self.vlayout = QtWidgets.QVBoxLayout(self)
        texting = "   " + self.id
        self.name = QtWidgets.QLabel(self.id)
        self.vlayout.addWidget(self.name, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.vlayout)
        
    def mousePressEvent(self, event:QtGui.QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.changepagebyesd.emit(self.dest)
            
    
            
def window():
    app = QtWidgets.QApplication([])
    window = ESD("0ESD021")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
