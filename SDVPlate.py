from PyQt6 import QtWidgets, QtGui, QtCore
from Store import Store
import os
import sys

class Valves(QtWidgets.QWidget):
    ValveChangingPos = QtCore.pyqtSignal(int)
    updatevalues = QtCore.pyqtSignal()
    def __init__(self,store:Store,variableid,value,title):
        super().__init__()
        self.setFixedSize(200,400)
        self.value = value
        self.variableid = variableid
        self.store = store
        self.title = title
        cd = os.getcwd()
        imgd = os.path.join(cd,"images")
        eqd = os.path.join(imgd,"equipment")
        icon = os.path.join(eqd,"ev2g1.png")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.setWindowTitle(self.variableid)
        self.name = QtWidgets.QLabel("0EV001",self)
        self.setFixedWidth(250)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self._InitUi()
        store.updatevalues.connect(self.ReadingValue)
        self.settingData()

    def _InitUi(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.vlayout)
        
    def settingData(self):
        name = " " + self.variableid
        title = QtWidgets.QLabel("",self)
        ftitle = " " + self.title 
        title.setText(ftitle)
        self.name.setText(name)
        self.name.setStyleSheet("font-weight:bold;size:14px")
        self.vlayout.addWidget(self.name)
        self.vlayout.addWidget(title)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.settingPV()

    def settingPV(self):
        self.radioGroupBox = QtWidgets.QGroupBox("PV",self)
        self.radioGroupBox.setStyleSheet("color:gray;")
        self.radioGroupBox.setEnabled(False)
        self.radioLayout = QtWidgets.QVBoxLayout()
        self.Openradio= QtWidgets.QRadioButton("OPEN",self)
        # self.Openradio.setStyleSheet
        self.Openradio.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: white;
                    border: 1px solid gray;
                    width: 10px;
                    height: 10px;;
                    border-radius: 15px;
                }
                QRadioButton::indicator:checked {
                    background-color: black;
                }
                QRadioButton::indicator:unchecked {
                    background-color: white;
                }
                """)
        self.Openradio.setChecked(True)
        self.Openradio.setEnabled(False)
        self.Closeradio= QtWidgets.QRadioButton("CLOSE",self)
        # self.Close
        self.Closeradio.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: white;
                    border: 1px solid gray;
                    width: 10px;
                    height: 10px;
                    border-radius: 15px;
                }
                QRadioButton::indicator:checked {
                    background-color: black;
                }
                QRadioButton::indicator:unchecked {
                    background-color: white;
                }
                """)
        self.Closeradio.setEnabled(False)
        self.radioLayout.addWidget(self.Openradio)
        self.radioLayout.addWidget(self.Closeradio)
        self.radioGroupBox.setLayout(self.radioLayout)
        self.vlayout.addWidget(self.radioGroupBox)
        self.settingOP()

    def settingOP(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.OP = QtWidgets.QLabel(" OP",self)
        self.OP.setStyleSheet("color:gray;")
        self.OPValue = QtWidgets.QLabel("",self)
        self.OPValue.setStyleSheet("""
            QLabel {
                color: black;
                font-weight: bold;
            }
        """)
        hlayout.addWidget(self.OP)
        hlayout.addWidget(self.OPValue)
        self.vlayout.addLayout(hlayout)
        self.settingOPvalue()
        self.btnChangingPos()
    
    def settingOPvalue(self):
        if self.value == 1:
            self.OPValue.setText("OPEN")
        else:
            self.OPValue.setText("CLOSE")

    def btnChangingPos(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.Close = QtWidgets.QPushButton("CLOSE",self)
        self.Open = QtWidgets.QPushButton("OPEN",self)
        hlayout.addWidget(self.Open)
        hlayout.addWidget(self.Close)
        self.vlayout.addLayout(hlayout)
        self.Open.clicked.connect(self.OpeningPosition)
        self.Close.clicked.connect(self.ClosingPostion)

    def OpeningPosition(self):
        self.store.settingValueOPC(self.variableid,1)
        self.OPValue.setText("OPEN")
        # self.Openradio.setChecked(True)
        # self.Closeradio.setChecked(False)
        
        # self.ValveChangingPos.emit(1)
        # print("Signal emitted: OpeningPosition")

    def ClosingPostion(self):
        self.store.settingValueOPC(self.variableid,2)
        self.OPValue.setText("CLOSE")
        # self.Closeradio.setChecked(True)
        # self.Openradio.setChecked(False)
        # self.ValveChangingPos.emit(2)
        # print("Signal emitted: ClosingPostion")
    
    @QtCore.pyqtSlot()
    def ReadingValue(self):
        value = self.store.finaltag[self.variableid]
        if value == 1:
            self.Openradio.setChecked(True)
            self.Closeradio.setChecked(False)
        if value == 2:
            self.Openradio.setChecked(False)
            self.Closeradio.setChecked(True)
        # print(f"{self.variableid}:{value}")
        # self.ValveChangingPos.emit(value)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Valves()
    # widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())