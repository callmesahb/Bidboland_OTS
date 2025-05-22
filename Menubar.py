from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import os

class Menu(QtWidgets.QWidget):
    def __init__(self,data):
        super().__init__()
        self.setStyleSheet("color:#cecece;")
        self.setWindowTitle("Menubar")
        current = os.getcwd()
        self.icondir = os.path.join(current,"icons")
        self.left = QtWidgets.QPushButton("",self)
        self.data = data
        self._InitUI()
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.vlayout)
        # self.setStyleSheet("background-color:#dbdab9;")
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("#cecece"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        # self.setFixedSize(200,1080)
        self.setFixedWidth(180)
        self.SettingButtons()
        
    def SettingButtons(self):
        hlayout = QtWidgets.QHBoxLayout()
        ovs = QtWidgets.QLabel("Overviews",self)
        ovs.setStyleSheet("color:black;")
        # hlayout.addWidget(ovs,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        vlayout = QtWidgets.QVBoxLayout()
        self.PRC = QtWidgets.QPushButton("PRC",self)
        self.PRC.setStyleSheet("color:black;")
        self.UTL = QtWidgets.QPushButton("UTL",self)
        self.UTL.setStyleSheet("color:black;")
        self.ESD = QtWidgets.QPushButton("ESD",self)
        self.ESD.setStyleSheet("color:black;")
        self.FGS = QtWidgets.QPushButton("FGS",self)
        self.FGS.setStyleSheet("color:black;")
        vlayout.addWidget(ovs,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self.PRC)
        hlayout.addWidget(self.ESD)
        hlayout.addWidget(self.UTL)
        hlayout.addWidget(self.FGS)
        vlayout.addLayout(hlayout)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addLayout(vlayout)
        self.vlayout.addWidget(hline)
        self.settingdetailsofpage()
        # self.PRC.clicked.connect(self.printing)
        # hlayout.addLayout(vlayout)
        
    def settingdetailsofpage(self):
        vlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        self.pagenum = QtWidgets.QLabel("CPR",self)
        self.pagenum.setStyleSheet("color:black;")
        self.desc = QtWidgets.QLabel("Regen",self)
        self.desc.setStyleSheet("color:black;")
        self.next = QtWidgets.QPushButton(">>",self)
        self.next.setStyleSheet("color:black;")
        self.back = QtWidgets.QPushButton("<<",self)
        self.back.setStyleSheet("color:black;")
        vlayout.addWidget(self.pagenum,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        vlayout.addWidget(self.desc,1,QtCore.Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(self.back)
        hlayout.addWidget(self.next)
        vlayout.addLayout(hlayout)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addLayout(vlayout)
        self.vlayout.addWidget(hline)
        self.SettingsPart()
    def buttonsofpage(self):
        # vlayout = QtWidgets.QVBoxLayout()
        # self.vlayout.addLayout(vlayout)
        self.SettingsPart()
    
    def SettingsPart(self):
        vvlayout = QtWidgets.QVBoxLayout()
        self.settings = QtWidgets.QLabel("Settings",self)
        self.settings.setStyleSheet("color:black;")
        self.settings.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        vvlayout.addWidget(self.settings)
        vvlayout.addWidget(hline)
        self.vlayout.addLayout(vvlayout)
        self.ChangingPageByFlash()
        

    def ChangingPageByFlash(self):
        hlayout = QtWidgets.QHBoxLayout()
        print("Runing")
        self.right = QtWidgets.QPushButton("",self)
        self.right.setStyleSheet("color:black;")
        
        self.left.setStyleSheet("color:black;")
        self.up = QtWidgets.QPushButton("",self)
        self.up.setStyleSheet("color:black;")
        # self.up.setFlat(True)
        self.up.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow-090.png")))
        self.right.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow.png")))
        self.left.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow-180.png")))
        hlayout.addWidget(self.left)
        hlayout.addWidget(self.up)
        hlayout.addWidget(self.right)
        self.vlayout.addLayout(hlayout)
        
        
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Menu("SOME DATA")
    window.show()
    sys.exit(app.exec())