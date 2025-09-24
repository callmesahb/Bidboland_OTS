from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import os

class Menu(QtWidgets.QWidget):
    changepage = QtCore.pyqtSignal(str)
    changepage1 = QtCore.pyqtSignal(str)
    changepage2 = QtCore.pyqtSignal(str)
    def __init__(self,data):
        super().__init__()
        self.setStyleSheet("color:#9c938e;")
        self.setWindowTitle("Menubar")
        current = os.getcwd()
        self.icondir = os.path.join(current,"icons")
        
        self.data = data
        self._InitUI()
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.vlayout)
        # self.setStyleSheet("background-color:#dbdab9;")
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("#9c938e"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        # self.setFixedSize(200,1080)
        self.setFixedWidth(210)
        self.SettingButtons()
    def Next(self):
        self.changepage.emit("NEXT")
        print("Emiting")
        
    def SettingButtons(self):
        hlayout = QtWidgets.QHBoxLayout()
        ovs = QtWidgets.QLabel("Overviews",self)
        ovs.setStyleSheet("color:black;font-size:16px;")
        # hlayout.addWidget(ovs,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        vlayout = QtWidgets.QVBoxLayout()
        self.PRC = QtWidgets.QPushButton("PRC",self)
        self.PRC.setStyleSheet("color:black;font-size:16px;")
        self.UTL = QtWidgets.QPushButton("UTL",self)
        self.UTL.setStyleSheet("color:black;font-size:16px;")
        self.ESD = QtWidgets.QPushButton("ESD",self)
        self.ESD.setStyleSheet("color:black;font-size:16px;")
        self.FGS = QtWidgets.QPushButton("FGS",self)
        self.FGS.setStyleSheet("color:black;font-size:16px;")
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
        self.pagenum.setStyleSheet("color:black;font-size:16px;")
        self.desc = QtWidgets.QLabel("Regen",self)
        self.desc.setStyleSheet("color:black;font-size:14px;")
        self.next = QtWidgets.QPushButton(">>",self)
        self.next.setStyleSheet("color:black;font-size:16px;")
        self.back = QtWidgets.QPushButton("<<",self)
        self.back.setStyleSheet("color:black;font-size:16px;")
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
        self.settings.setStyleSheet("color:black;font-size:16px;")
        self.settings.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        vvlayout.addWidget(self.settings)
        vvlayout.addWidget(hline)
        self.vlayout.addLayout(vvlayout)
        self.ChangingPageByFlash()
        
    def Right(self):
        self.changepage.emit("NEXT")
    def Back(self):
        self.changepage1.emit("BACK")
    def Up(self):
        self.changepage2.emit("UP")
    def ChangingPageByFlash(self):
        hlayout = QtWidgets.QHBoxLayout()
        print("Runing")
        self.right = QtWidgets.QPushButton("",self)
        self.right.setStyleSheet("color:black;font-size:16px;")
        self.right.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow.png")))
        self.right.clicked.connect(self.Right)
        self.left = QtWidgets.QPushButton("",self)
        self.left.clicked.connect(self.Back)
        self.left.setStyleSheet("color:black;font-size:16px;")
        self.left.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow-180.png")))
        self.up = QtWidgets.QPushButton("",self)
        self.up.setStyleSheet("color:black;font-size:16px;")
        self.up.clicked.connect(self.Up)
        # self.up.setFlat(True)
        self.up.setIcon(QtGui.QIcon(os.path.join(self.icondir,"arrow-090.png")))

        hlayout.addWidget(self.left)
        hlayout.addWidget(self.up)
        hlayout.addWidget(self.right)
        self.vlayout.addLayout(hlayout)
        
        
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Menu("SOME DATA")
    window.show()
    sys.exit(app.exec())