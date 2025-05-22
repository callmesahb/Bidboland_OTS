from PyQt6 import QtWidgets, QtGui, QtCore
from Store import Store
import sys

class PumpFacePlate(QtWidgets.QWidget):
    PumpChangingPos = QtCore.pyqtSignal(str)
    
    def __init__(self, variableid=None, store: Store = None):
        super().__init__()
        self.setWindowTitle("Pump")
        self.setFixedWidth(200)
        self.variableid = variableid
        self.store = store
        self._InitUI()
        self.settingdata()
    
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)
        
    def settingdata(self):
        self.pname = QtWidgets.QLabel("")
        self.pname.setText(str(self.variableid))
        self.vlayout.addWidget(self.pname)
        
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        
        self.settingPV()

    def settingPV(self):
        self.radioGroupBox = QtWidgets.QGroupBox("PV                                                   OP", self)
        self.radioGroupBox.setStyleSheet("color:gray;")
        
        self.radioLayout = QtWidgets.QGridLayout()
        
        self.OPOPEN = QtWidgets.QCheckBox("", self)
        self.OPCLOSE = QtWidgets.QCheckBox("", self)
        self.Runradio = QtWidgets.QRadioButton("RUN", self)
        self.Runradio.setStyleSheet("color:black;")
        self.Runradio.setChecked(True)
        self.Runradio.setEnabled(False)
        self.Stopradio = QtWidgets.QRadioButton("STOP", self)
        self.Stopradio.setStyleSheet("color:black;")
        self.Stopradio.setEnabled(False)
        self.radioLayout.addWidget(self.OPOPEN, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.OPCLOSE, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.Runradio, 0, 0)
        self.radioLayout.addWidget(self.Stopradio, 1, 0)

        self.radioGroupBox.setLayout(self.radioLayout)
        self.vlayout.addWidget(self.radioGroupBox)
        
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        
        self.ChangingPos()
        
    def ChangingPos(self):
        vlayout = QtWidgets.QVBoxLayout()
        vvlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        
        # remote/local radio
        self.remotelocal = QtWidgets.QRadioButton("LOCALMAN", self)
        self.remotelocal.toggled.connect(self.handleRemoteLocalToggle)
        
        pv = QtWidgets.QLabel("PV", self)
        pv.setStyleSheet("color:gray;")
        op = QtWidgets.QLabel("OP", self)
        op.setStyleSheet("color:gray;")
        
        self.pvvalue = QtWidgets.QLabel("", self)
        self.opvalue = QtWidgets.QComboBox(self)
        self.opvalue.addItems(["RUN", "STOP"])
        self.opvalue.currentTextChanged.connect(self.ChangingPosFunc)
        
        vlayout.addWidget(self.remotelocal)
        vlayout.addWidget(pv)
        vlayout.addWidget(op)
        vvlayout.addWidget(self.pvvalue)
        vvlayout.addWidget(self.opvalue)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vvlayout)
        
        self.vlayout.addLayout(hlayout)
        
        self.pvvalue.setText(self.opvalue.currentText())
        
        # حالت اولیه غیرفعال باشه
        self.opvalue.setEnabled(self.remotelocal.isChecked())

    def handleRemoteLocalToggle(self, checked):
        self.opvalue.setEnabled(checked)

    def ChangingPosFunc(self):
        self.pvvalue.setText(self.opvalue.currentText())
        
        if self.opvalue.currentText() == "STOP":
            self.Stopradio.setChecked(True)
            self.OPCLOSE.setChecked(True)
            self.Runradio.setChecked(False)
            self.OPOPEN.setChecked(False)
            if self.store:
                self.store.settingValueOPC(self.variableid, 2)
        
        elif self.opvalue.currentText() == "RUN":
            self.Stopradio.setChecked(False)
            self.OPCLOSE.setChecked(False)
            self.Runradio.setChecked(True)
            self.OPOPEN.setChecked(True)
            self.PumpChangingPos.emit("RUN")
            if self.store:
                self.store.settingValueOPC(self.variableid, 1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PumpFacePlate("Pump_101", Store())  # مقدار فرضی برای تست
