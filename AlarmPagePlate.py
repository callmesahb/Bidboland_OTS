from PyQt6 import QtWidgets, QtGui, QtCore
from controllerbar import TriangleWidget
from ProgressWidget import TriangleWidgetNew
import sys
import os
from Store import Store
class Sensor(QtWidgets.QWidget):
    pvstatus = QtCore.pyqtSignal(str)
    def __init__(self,store:Store,name,variableid,ranges,title,type):
        updatevalues = QtCore.pyqtSignal(dict,list)
        super().__init__()
        self.setWindowTitle("")
        self.name = name
        self.store = store
        self.title = title
        self.type = type
        cd = os.getcwd()
        self.imgdir = os.path.join(cd,"icons")
        self.variableid = variableid
        self.ranges = ranges
        self.notnames = ["1FI003B","1FI006","1FI005B","4201LI009","1LI062","1FI026"]
        self.setFixedWidth(250)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.details = self.store.SettingDetailsofsensor(variableid)
        self.unit = self.store.GettingUnit(variableid)
        self.finalunit = " " + self.unit
        self.store.updatevalues.connect(self.updatingvalue)
        self._InitUI()
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.vlayout)
        self.settingname()
        
    
    def settingname(self):
        self.sensorname = QtWidgets.QLabel("", self)
        self.sensorname.setStyleSheet("font-weight:bold;font-size:26px;")
        self.vlayout.addWidget(self.sensorname,0,QtCore.Qt.AlignmentFlag.AlignVCenter)
        name =self.variableid
        self.sensorname.setText(name)
        self.ftitle = QtWidgets.QLabel("",self)
        ftitle = self.title
        self.ftitle.setText(ftitle)
        self.ftitle.setStyleSheet("font-size:26px")
        self.vlayout.addWidget(self.ftitle)
        ex1 = QtWidgets.QLabel("",self)
        ex1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.vlayout.addWidget(ex1)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        ex1 = QtWidgets.QLabel("",self)
        ex1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.vlayout.addWidget(ex1)
        self.settingProgressbar()
    
        
    def settingProgressbar(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.Unittag = QtWidgets.QLabel("",self)
        self.Unittag.setText(self.finalunit)
        hlayout.addWidget(self.Unittag)
        self.Progressbar = TriangleWidget(self.ranges[2],self.ranges[4],self.ranges[5],self.ranges[3],self.variableid,self.store,self.ranges)
        self.store.updatevalues.connect(self.Progressbar.settingrangesensor)
        self.Progressbar.rightProgress.setHidden(True)
        self.Progressbar.setminmaxvalue(self.ranges[0],self.ranges[1])
        if self.name in self.notnames:
            self.Progressbar = TriangleWidgetNew(self.ranges[2],self.ranges[4],self.ranges[5],self.ranges[3],self.variableid,self.store)
            self.store.updatevalues.connect(self.Progressbar.settingrangesensor)
            self.Progressbar.rightProgress.setHidden(True)
            self.Progressbar.setminmaxvalue(self.ranges[0],self.ranges[1])
            height = self.Progressbar.progress.height()
            step = (height-12) // 4
            self.Progressbar.setFixedHeight(220)
            self.Progressbar.setFixedWidth(80)
            self.Progressbar.label1.setGeometry(0, 11, 50, 20)
            self.Progressbar.label2.setGeometry(0, 12+step, 50, 20)
            self.Progressbar.label3.setGeometry(0, 12+2*step, 50, 20)
            self.Progressbar.label4.setGeometry(0,12+3*step, 50, 20)
            self.Progressbar.label5.setGeometry(0, 12+4*step, 50, 20)
        else:
            self.Progressbar = TriangleWidget(self.ranges[2],self.ranges[4],self.ranges[5],self.ranges[3],self.variableid,self.store,self.ranges)
            self.store.updatevalues.connect(self.Progressbar.settingrangesensor)
            self.Progressbar.rightProgress.setHidden(True)
            self.Progressbar.setminmaxvalue(self.ranges[0],self.ranges[1])
            height = self.Progressbar.progress.height()
            step = (height-12) // 4
            self.Progressbar.setFixedHeight(220)
            self.Progressbar.label1.setGeometry(5, 11, 50, 20)
            self.Progressbar.label2.setGeometry(5, 12+step, 50, 20)
            self.Progressbar.label3.setGeometry(5, 12+2*step, 50, 20)
            self.Progressbar.label4.setGeometry(5,12+3*step, 50, 20)
            self.Progressbar.label5.setGeometry(5, 12+4*step, 50, 20)
        # self.Progressbar.progress.setValue(int(self.value))
        # self.Progressbar.setRightValue(int(self.value))
        hlayout.addWidget(self.Progressbar)
        self.vlayout.addLayout(hlayout)
        ex1 = QtWidgets.QLabel("",self)
        ex1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.vlayout.addWidget(ex1)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        # self.SettingValue()
        
        self.PVstatus()
    def PVstatus(self):
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.status = QtWidgets.QLabel("",self)
        self.icon = QtWidgets.QLabel()
        hlayout.addWidget(self.icon)
        for i in range(0,5):
            status = QtWidgets.QLabel()
            hlayout.addWidget(status)
            i = i+1
        self.status.setStyleSheet("font-weight:bold; font-size:14px;padding:0px; margin:0px;")
        # hlayout.addWidget(self.status)
        self.vlayout.addLayout(hlayout)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.SettingValue()
    def SettingValue(self):
        hlayout_op = QtWidgets.QHBoxLayout()
        hlayout_op.setSpacing(2)
        hlayout_op.setContentsMargins(0, 0, 0, 0)
        self.PV = QtWidgets.QLabel("PV", self)
        self.PV.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.PV.setStyleSheet("font-size:14px; padding: 0px; margin: 0px;")
        self.PVLine = QtWidgets.QLabel("", self)
        self.PVLine.setStyleSheet("background-color: #00ff01;")
        self.PVLine.setFixedWidth(3)
        self.PVValue = QtWidgets.QLabel("120", self)
        self.PVValue.setStyleSheet("font-weight:bold;font-size:18px")
        # self.PVValue.setText(str(self.value))
        ex1 = QtWidgets.QLabel("",self)
        ex1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        # self.vlayout.addWidget(ex1)
        hlayout_op.addWidget(self.PV)
        hlayout_op.addWidget(self.PVLine,0,QtCore.Qt.AlignmentFlag.AlignLeft)
        hlayout_op.addWidget(self.PVValue)
        self.vlayout.addLayout(hlayout_op)
        ex1 = QtWidgets.QLabel("",self)
        ex1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Expanding)
        self.vlayout.addWidget(ex1)
    
    @QtCore.pyqtSlot()
    def updatingvalue(self):
        value = self.store.finaltag[self.variableid]
        pvl = self.variableid + "PVL"
        pvll = self.variableid + "PVLL"
        pvh = self.variableid + "PVH"
        pvhh = self.variableid + "PVHH"
        pvlv = self.store.finaltag[pvl]
        pvllv = self.store.finaltag[pvll]
        pvhv = self.store.finaltag[pvh]
        pvhhv = self.store.finaltag[pvhh]
        if value >= self.ranges[1]:
            value=self.ranges[1]
        self.fvalue = self.Progressbar.value_to_percent(value)
        self.Progressbar.progress.setValue(int(self.fvalue))
        self.PVValue.setText(str(round(value,2)))
        if value < pvhhv and value >= pvhv:
            self.pvstatus.emit("H ALARM")
            self.Progressbar.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    background-color: black;
                    border-radius: 5px;
                }
                QProgressBar::chunk {
                    background-color: #fffc00;
                }
            """)
            self.icon.setPixmap(QtGui.QPixmap(os.path.join(self.imgdir,"exhi.png")))
        elif value >= pvhhv and value <= self.ranges[1]:
            self.pvstatus.emit("HH ALARM")

            self.Progressbar.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    background-color: black;
                    border-radius: 5px;
                }
                QProgressBar::chunk {
                    background-color: #fffc00;
                }
            """)
            self.icon.setPixmap(QtGui.QPixmap(os.path.join(self.imgdir,"exhi.png")))
        elif value <= pvlv and value > pvllv:
            self.pvstatus.emit("L ALARM")

            self.Progressbar.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    background-color: black;
                    border-radius: 5px;
                }
                QProgressBar::chunk {
                    background-color: #fffc00;
                }
            """)
            self.icon.setPixmap(QtGui.QPixmap(os.path.join(self.imgdir,"exclamationmark.png")))
        elif value <= pvllv and value >= self.ranges[0]:
            self.pvstatus.emit("LL ALARM")
            self.Progressbar.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    background-color: black;
                    border-radius: 5px;
                }
                QProgressBar::chunk {
                    background-color: #fffc00;
                }
            """)
            self.icon.setPixmap(QtGui.QPixmap(os.path.join(self.imgdir,"exclamationmark.png")))
        elif value > pvlv and value < pvhv:
            self.pvstatus.emit("NORMAL")
            self.Progressbar.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: rgb(0,255,1);
            }
        """)
            self.icon.setPixmap(QtGui.QPixmap())
        self.update()
        # self.Progressbar.setCentervalue(int(value))
        # self.Progressbar.progress.setValue(int(self.fvalue))
        # self.Progressbar.setRightValue(int(value))
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Sensor()
    window.show()
    sys.exit(app.exec())