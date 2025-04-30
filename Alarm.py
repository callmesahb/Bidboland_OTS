from PyQt6 import QtWidgets,QtCore,QtGui
from Store import Store
import sys

class Alarm(QtWidgets.QWidget):
    alarmtriggered = QtCore.pyqtSignal(str)
    alarmresult = QtCore.pyqtSignal()
    def __init__(self,variableid:str,store:Store):
        super().__init__()
        self.variableid = variableid
        self.store = store
        self.status = QtWidgets.QLabel("NORMAL",self)
        self.status.setStyleSheet("color:#28da48;")
        self.status.move(18,3)
        self.setStyleSheet("background-color:#000000")
        # self._InitUI()
        
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.addWidget(self.status,0,QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vlayout)
        
    
    @QtCore.pyqtSlot()
    def updateAlarm(self):
        value = self.store.finaltag[self.variableid]
        if value < self.store.SettingDetailsofsensor(self.variableid)[2]: # Less than LL
            self.status.setText("ALARM")
            self.status.setStyleSheet("color:red")
            self.alarmtriggered.emit("ALARM")
        else:
            self.status.setText("NORMAL")
            self.status.setStyleSheet("color:#28da48")
            self.alarmtriggered.emit("NORMAL")
        
        
if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Alarm()
        window.show()
        sys.exit(app.exec())