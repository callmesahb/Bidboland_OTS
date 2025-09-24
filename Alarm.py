from PyQt6 import QtWidgets,QtCore,QtGui
from Store import Store
import sys

class Alarm(QtWidgets.QWidget):
    alarmstatus = QtCore.pyqtSignal(str)
    alarmtriggered = QtCore.pyqtSignal(str)
    alarmresult = QtCore.pyqtSignal()
    alarmstatus2 = QtCore.pyqtSignal(str)
    def __init__(self,variableid:str,store:Store,id:str):
        super().__init__()
        self.variableid = variableid
        self.store = store
        self.id = id
        self.status = QtWidgets.QLabel("NORMAL",self)
        self.status.setStyleSheet("color:#28da48;")
        self.status.move(18,3)
        self.setStyleSheet("background-color:#000000")
        
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.addWidget(self.status,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vlayout)
        
    # LAHH
    # LALL
    @QtCore.pyqtSlot()
    def updateAlarm(self):
        value = self.store.finaltag[self.variableid]
        pvll = self.variableid + "PVLL"
        pvhh = self.variableid + "PVHH"
        pvllv = self.store.finaltag[pvll]
        pvhhv = self.store.finaltag[pvhh]
        if self.id[3] == "L":
            if value <pvllv: # Less than LL
                self.status.setText("ALARM")
                self.status.setStyleSheet("color:red")
                self.alarmtriggered.emit("ALARM")
                emitid = self.id + "L"
                self.store.settingValueOPC(emitid,2)
                self.alarmstatus.emit(emitid)
            else:
                self.status.setText("NORMAL")
                self.status.setStyleSheet("color:#28da48")
                emitid = self.id + "L"
                self.store.settingValueOPC(emitid,1)
                self.alarmstatus.emit(emitid)
                self.alarmtriggered.emit("NORMAL")
        elif self.id[3] == "H":
            if value > pvhhv: # Less than LL
                self.status.setText("ALARM")
                self.status.setStyleSheet("color:red")
                self.alarmtriggered.emit("ALARM")
                emitid = self.id + "L"
                self.store.settingValueOPC(emitid,2)
                self.alarmstatus.emit(emitid)
            else:
                self.status.setText("NORMAL")
                self.status.setStyleSheet("color:#28da48")
                emitid = self.id + "L"
                self.store.settingValueOPC(emitid,1)
                self.alarmstatus.emit(emitid)
                self.alarmtriggered.emit("NORMAL")
        
        
if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Alarm()
        window.show()
        sys.exit(app.exec())