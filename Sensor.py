from PyQt6 import QtWidgets, QtGui, QtCore
from controllerbar import TriangleWidget
from ProgressWidget import TriangleWidgetNew
import sys
from Store import Store
from AlarmPanel import AlarmPanel
class Sensor(QtWidgets.QWidget):
    def __init__(self,value,store:Store,name,variableid:str,ranges,title,type):
        updatevalues = QtCore.pyqtSignal(dict,list)
        super().__init__()
        self.setWindowTitle("")
        self.value = value
        self.name = name
        self.store = store
        self.title = title
        self.type = type
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
        self.sensorname = QtWidgets.QPushButton("", self)
        self.sensorname.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: black;
                text-align: left;
                font-weight:bold;
            }
            QPushButton:hover {
                color: blue;
            }
        """)
        self.sensorname.clicked.connect(self.printname)
        self.vlayout.addWidget(self.sensorname,0,QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ftitle = QtWidgets.QLabel("",self)
        # if self.variableid.startswith("4201LI0"):
        #     ftitle = " On " + self.title
        ftitle = " " + self.title
        self.ftitle.setText(ftitle)
        self.vlayout.addWidget(self.ftitle)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.settingProgressbar()
    
    def printname(self):
        self.contpage = AlarmPanel(self.type,self.variableid,self.store,self.ranges,self.name,self.title)
        # self.contpage.setFixedSize(1200,1200)
        self.contpage.show()
        self.close()
        
    def settingProgressbar(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.Unittag = QtWidgets.QLabel("",self)
        self.Unittag.setText(self.finalunit)
        hlayout.addWidget(self.Unittag)
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
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)
        self.SettingValue()
    
    def SettingValue(self):
        hlayout_op = QtWidgets.QHBoxLayout()
        self.PV = QtWidgets.QLabel(" PV", self)
        self.PVValue = QtWidgets.QLabel("120", self)
        self.PVValue.setText(str(self.value))
        hlayout_op.addWidget(self.PV)
        hlayout_op.addWidget(self.PVValue)
        self.vlayout.addLayout(hlayout_op)
    
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
        if value > self.ranges[1]:
            value = self.ranges[1]
        self.fvalue = self.Progressbar.value_to_percent(value)
        self.Progressbar.progress.setValue(int(self.fvalue))
        self.PVValue.setText(str(round(value,2)))
        if value >= pvhv and value < pvhhv:
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
        elif value >= pvhhv and value <= self.ranges[1]:
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
        elif value <= pvlv and value > pvllv:
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
        elif value <= pvllv and value >= self.ranges[0]:
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
        elif value > pvlv and value < pvhv:
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
        self.update()
        # self.Progressbar.setCentervalue(int(value))
        # self.Progressbar.progress.setValue(int(self.fvalue))
        # self.Progressbar.setRightValue(int(value))
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Sensor()
    window.show()
    sys.exit(app.exec())