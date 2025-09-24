from PyQt6 import QtWidgets, QtGui, QtCore
from Store import Store
import sys

class PumpFacePlate(QtWidgets.QWidget):
    PumpChangingPos = QtCore.pyqtSignal(str)
    
    def __init__(self, variableid=None, store: Store = None,title = None):
        super().__init__()
        self.setWindowTitle("Pump")
        self.setFixedWidth(250)
        self.variableid = variableid
        self.store = store
        self.title = title
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.store.updatevalues.connect(self.ReadValue)
        self._InitUI()
        self.settingdata()
    
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.vlayout)
        
    def settingdata(self):
        self.pname = QtWidgets.QLabel("")
        pname = " " + self.variableid
        self.wtitle = QtWidgets.QLabel("",self)
        ftitle = " " + self.title
        self.wtitle.setText(str(ftitle))
        self.pname.setText(str(pname))
        self.vlayout.addWidget(self.pname)
        self.vlayout.addWidget(self.wtitle)
        
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
        self.OPOPEN.setEnabled(False)
        self.OPCLOSE = QtWidgets.QCheckBox("", self)
        self.OPCLOSE.setEnabled(False)
        self.Runradio = QtWidgets.QRadioButton("RUN", self)
        self.Runradio.setStyleSheet("""
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
        self.Runradio.setChecked(False)
        self.Runradio.setEnabled(False)
        self.Stopradio = QtWidgets.QRadioButton("STOP", self)
        self.Stopradio.setStyleSheet("""
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
        self.Stopradio.setEnabled(False)
        self.radioLayout.addWidget(self.OPOPEN, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.OPCLOSE, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.Runradio, 0, 0)
        self.radioLayout.addWidget(self.Stopradio, 1, 0)

        self.radioGroupBox.setLayout(self.radioLayout)
        self.vlayout.addWidget(self.radioGroupBox)
        

        
        self.rl()
    def rl(self):
        # self.radioGroupBox = QtWidgets.QGroupBox(self)
        # self.radioLayout = QtWidgets.QGridLayout()
        
        self.remoteradio = QtWidgets.QRadioButton("Remote\Local", self)
        self.remoteradio.setStyleSheet("color:gray;")
        self.remoteradio.setChecked(True)
        self.remoteradio.setEnabled(False)

        self.radioLayout.addWidget(self.remoteradio, 2, 0)


     


        self.ChangingPos()


        
    def ChangingPos(self):
        vlayout = QtWidgets.QVBoxLayout()
        vvlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        
        # remote/local radio
        
        pv = QtWidgets.QLabel("PV", self)
        pv.setStyleSheet("color:gray;")
        op = QtWidgets.QLabel("OP", self)
        op.setStyleSheet("color:gray;")
        
        self.pvvalue = QtWidgets.QLabel("", self)
        self.opvalue = QtWidgets.QComboBox(self)
        # self.opvalue.addItems()
        self.opvalue.currentTextChanged.connect(self.ChangingPosFunc)

        vlayout.addWidget(pv)
        vlayout.addWidget(op)
        vvlayout.addWidget(self.pvvalue)
        vvlayout.addWidget(self.opvalue)
        
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vvlayout)
        
        self.vlayout.addLayout(hlayout)
        
        self.pvvalue.setText(self.opvalue.currentText())
        

    def handleRemoteLocalToggle(self, checked):
        self.opvalue.setEnabled(checked)

    def ChangingPosFunc(self):
        self.pvvalue.setText(self.opvalue.currentText())
        
        if self.opvalue.currentText() == "STOP":
            self.store.settingValueOPC(self.variableid, 2)
        
        elif self.opvalue.currentText() == "RUN":
            self.PumpChangingPos.emit("RUN")
            self.store.settingValueOPC(self.variableid, 1)
    @QtCore.pyqtSlot()
    def ReadValue(self):
        value = self.store.finaltag[self.variableid]
        target_items = []
        current_items = [self.opvalue.itemText(i) for i in range(self.opvalue.count())]
        if value == 1:
            self.pvvalue.setText("RUN")
            self.Stopradio.setChecked(False)
            self.OPCLOSE.setChecked(False)
            self.Runradio.setChecked(True)
            self.OPOPEN.setChecked(True)
            target_items = ["RUN","STOP"]
        elif value == 2:
            self.pvvalue.setText("STOP")
            self.Stopradio.setChecked(True)
            self.OPCLOSE.setChecked(True)
            self.Runradio.setChecked(False)
            self.OPOPEN.setChecked(False)
            target_items = ["STOP","RUN"]
        for item in target_items:
            if item not in current_items:
                self.opvalue.addItem(item)
        for item in current_items:
            if item not in target_items:
                index = self.opvalue.findText(item)
                if index >= 0:
                    self.opvalue.removeItem(index)
        self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PumpFacePlate("Pump_101", Store())
