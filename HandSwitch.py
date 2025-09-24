from PyQt6 import QtWidgets,QtCore
import sys
from Store import Store

class HandSwitch(QtWidgets.QWidget):
    def __init__(self,name,btns,store:Store):
        super().__init__()
        self.setWindowTitle("HandSwitch")
        self.name = name
        self.btns = btns
        self.store = store
        self.store.updatevalues.connect(self.updatevalue)
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.ChangeHand)
        # self.timer.start(2000)
        self._InitUI()
        self.settingdata()
        
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(4,0,2,2)
        self.setLayout(self.vlayout)
        
    def settingdata(self):
        self.hname = QtWidgets.QLabel("403ARSP001A")
        self.vlayout.addWidget(self.hname)
        self.hname.setText(" " + self.name)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.settingPV()
    
    def settingPV(self):
        self.radioGroupBox = QtWidgets.QGroupBox("PV                                                                 OP", self)
        self.radioGroupBox.setStyleSheet("color:gray;")
        
        self.radioLayout = QtWidgets.QGridLayout()
        
        self.OPOPEN = QtWidgets.QCheckBox("", self)
        self.OPOPEN.setEnabled(False)
        # self.OPOPEN.setChecked(True)
        self.OPCLOSE = QtWidgets.QCheckBox("", self)
        self.OPCLOSE.setEnabled(False)
        self.Runradio = QtWidgets.QRadioButton(self.btns[0], self)
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
        self.Runradio.setEnabled(False)
        self.Stopradio = QtWidgets.QRadioButton(self.btns[1], self)
        self.Stopradio.setEnabled(False)
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
        self.OPOPEN.setChecked(False)
        
        self.radioLayout.addWidget(self.OPOPEN, 0, 1,QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.OPCLOSE, 1, 1,QtCore.Qt.AlignmentFlag.AlignRight)
        self.radioLayout.addWidget(self.Runradio, 0, 0)
        self.radioLayout.addWidget(self.Stopradio, 1, 0)

        self.radioGroupBox.setLayout(self.radioLayout)
        self.vlayout.addWidget(self.radioGroupBox)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.Switch()
    def Switch(self):
        vlayout = QtWidgets.QVBoxLayout()
        vvlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        pv = QtWidgets.QLabel("PV",self)
        pv.setStyleSheet("color:gray;")
        op = QtWidgets.QLabel("OP",self)
        op.setStyleSheet("color:gray;")
        self.pvvalue = QtWidgets.QLabel("",self)
        self.opvalue = QtWidgets.QComboBox(self)
        self.opvalue.addItems(["", ""])
        # self.opvalue.setEnabled(False)
        vlayout.addWidget(pv)
        vlayout.addWidget(op)
        # print(self.btns[0])
        # self.opvalue.setItemText(0,self.btns[0])
        # self.opvalue.setItemText(1,self.btns[1])
        vvlayout.addWidget(self.pvvalue)
        vvlayout.addWidget(self.opvalue)
        hlayout.addLayout(vlayout)
        hlayout.addLayout(vvlayout)
        self.vlayout.addLayout(hlayout)
        self.pvvalue.setText(self.opvalue.currentText())
        # self.opvalue.setDisabled(True)
        self.opvalue.currentTextChanged.connect(self.SwitchStruct)
        self.opvalue.currentTextChanged.connect(self.ChangeHand)
        
    def ChangeHand(self):
        text = self.opvalue.currentText()
        # self.opvalue.blockSignals(True)
        if text == str(self.btns[0]):
            self.store.settingValueOPC(self.name,1)
            # self.opvalue.clear()
            # self.opvalue.addItems(["4201FIC002", "4201PIC002"])
            # self.opvalue.setCurrentText("4201FIC002")
            # self.opvalue.blockSignals(False)
        elif text == str(self.btns[1]):
            self.store.settingValueOPC(self.name,2)
            # self.opvalue.clear()
            # self.opvalue.addItems(["4201PIC002", "4201FIC002"])
            # self.opvalue.setCurrentText("4201PIC002")
        # self.opvalue.blockSignals(False)
        
        

        
    def SwitchStruct(self):
        # self.pvvalue.setText(self.opvalue.currentText())
        # if self.opvalue.currentText() == self.opvalue.itemText(1):
        #     self.Stopradio.setChecked(True)
        #     self.OPCLOSE.setChecked(True)
        #     self.Runradio.setChecked(False)
        #     self.OPOPEN.setChecked(False)
        #     # self.PumpChangingPos.emit("STOP")
        
        # if self.opvalue.currentText() == self.opvalue.itemText(0):
        #     self.Stopradio.setChecked(False)
        #     self.OPCLOSE.setChecked(False)
        #     self.Runradio.setChecked(True)
        #     self.OPOPEN.setChecked(True)
        pass
            # self.PumpChangingPos.emit("RUN")
            
    @QtCore.pyqtSlot()
    def updatevalue(self):
        varid = self.name
        value = self.store.finaltag[varid]
        current_items = [self.opvalue.itemText(i) for i in range(self.opvalue.count())]
        target_items = []
        
        if value == 1:
            target_items = [str(self.btns[0]),str(self.btns[1])]
            self.Stopradio.setChecked(False)
            self.OPCLOSE.setChecked(False)
            self.Runradio.setChecked(True)
            self.OPOPEN.setChecked(True)
            self.pvvalue.setText(f"{str(self.btns[0])}")
        elif value == 2:
            target_items = [str(self.btns[1]),str(self.btns[0])]
            self.Stopradio.setChecked(True)
            self.OPCLOSE.setChecked(True)
            self.Runradio.setChecked(False)
            self.OPOPEN.setChecked(False)
            self.pvvalue.setText(f"{str(self.btns[1])}")
        
        for item in current_items:
            if item not in target_items:
                index = self.opvalue.findText(item)
                if index >= 0:
                    self.opvalue.removeItem(index)
        for item in target_items:
            if item not in current_items:
                self.opvalue.addItem(item)
        self.update()
    
if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = HandSwitch()
        window.show()
        sys.exit(app.exec())