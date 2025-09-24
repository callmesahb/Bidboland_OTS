import sys
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt
from IndicatorValue import IndicatorValue
from ControllerPlate import ControllerPlate
from Sensor import Sensor
from Store import Store
from Trend import Trend
class Indicator(QtWidgets.QWidget):
    updatevalues = QtCore.pyqtSignal(dict,list)
    TrendRequested = QtCore.pyqtSignal(str)
    prdstatussignal = QtCore.pyqtSignal(list)
    changingrewindstatus = QtCore.pyqtSignal(bool)
    
    def __init__(self,name,value,itype,pvvalues,store:Store,variableid:str,ranges:list,title:str,w):
        super().__init__()
        self.setStyleSheet("background-color:black")
        self.name = name
        self.value = value
        self.itype = itype
        self.pvvalues = pvvalues
        self.store = store
        self.variableid = variableid
        self.ranges = ranges
        self.w = w
        self.title = title
        # self.setMinimumSize(80,50)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.InitUI()
        
        
    def InitUI(self):
        self.hlayout = QtWidgets.QVBoxLayout()
        
        self.settingValue()
    def settingValue(self):
        self.Value = QtWidgets.QLabel("245",self)
        # if self.w > 65:
        #     self.Value.move(self.w-50,0)
        # elif self.w >= 60 or self.w <= 65:
        #     self.Value.move(self.w-20,0)
        # else:
        #     self.Value.move(self.w-40,0)
        self.Value.setFixedWidth(110)
        self.Value.move(6,0)
        self.status = QtWidgets.QLabel("",self)
        self.status.move(self.w - 20,1)
        self.status.setFixedWidth(20)
        # self.Value.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.hlayout.addWidget(self.Value)
        # self.Value.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.hlayout.addWidget(self.status)
        # self.setLayout(self.hlayout)
        if self.itype == "":
            self.Value.setText(str(round(self.value,2)))
        if self.itype == "controller":
            self.Value.setText(str(round(self.pvvalues[1],2)))
        self.Value.setStyleSheet("color:#40d964; font-size:14px;")
        
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.itype == "controller":
                self.finaltext = " " + self.variableid
                self.contplate = ControllerPlate(self.name,self.pvvalues,self.variableid,self.store,self.ranges,self.title,self.itype)
                self.contplate.prdopening.connect(self.prdstatus)
                pvname = self.variableid + "PV"
                unittag = self.store.GettingUnit(pvname)
                unit = " " + unittag
                self.contplate.Unittag.setText(unit)
                self.contplate.namee.setText(self.finaltext)
                self.contplate.show()
            if self.itype == "":
                if self.name == "0SIC001A" or self.name == "0SIC001B":
                    pass
                else:
                    unittag = self.store.GettingUnit(self.variableid)
                    unit = " " + unittag
                    self.sensor = Sensor(self.value,self.store,self.name,self.variableid,self.ranges,self.title,self.itype)
                    self.sensor.setWindowTitle(self.variableid)
                    self.finaltext = " " + self.variableid
                    self.sensor.sensorname.setText(self.finaltext)
                    # self.sensor.unittag.setText(unit)
                    self.sensor.show()
    
    @QtCore.pyqtSlot()
    def updatinvalue(self):
        if self.itype == "":
            value = self.store.finaltag[self.variableid]
            pvl = self.variableid + "PVL"
            pvh = self.variableid + "PVH"
            pvll = self.variableid + "PVLL"
            pvhh = self.variableid + "PVHH"
            pvlv = self.store.finaltag[pvl]
            pvhv = self.store.finaltag[pvh]
            pvllv = self.store.finaltag[pvll]
            pvhhv = self.store.finaltag[pvhh]
            if value > self.ranges[1]:
                value = self.ranges[1]
            if value < self.ranges[0]:
                value = self.ranges[0]
            if self.name[1] == "T":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.1f}")
            if self.name[1] == "L":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.1f}")
            if self.name[1] == "P":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.2f}")
            if self.name[1] == "A":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.2f}")
            if self.name == "1FEED_RATIO":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.2f}")
            if self.name == "4201LI009":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                self.Value.setText(f"{value:.1f}")
            
            

                
                
            if self.name[1] == "F":
                unit = self.store.GettingUnit(self.variableid)
                if unit == "Nm3/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    self.Value.setText(f"  {value:.3f}")
                elif unit == "kg/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    self.Value.setText(f"{value:.1f}")
                elif unit == "T/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    self.Value.setText(f"{value:.1f}")
                
            if value < pvlv and value > pvllv:  #Between LL and L
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
                self.status.setText("L")
                self.status.setStyleSheet("QLabel { color: #FFFF00; }")
            elif value <= pvllv and value >= self.store.SettingDetailsofsensor(self.variableid)[0]: # Less than LL
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
                self.status.setText("LL")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")
            elif value >= pvhv and value < pvhhv: # Between H & HH
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
                self.status.setText("H")
                self.status.setStyleSheet("QLabel { color: #FFFF00; }")
            elif value >= pvhhv and value <= self.store.SettingDetailsofsensor(self.variableid)[1]: #greater than HH
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
                self.status.setText("HH")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")


            else: # Normal
                self.Value.setStyleSheet("color:#40d964; font-size:14px;")
                self.status.setStyleSheet("QLabel { color: black; }")
        if self.itype == "controller":
            varid = self.variableid + "PV"
            unit = self.store.GettingUnit(varid)
            value = self.store.finaltag[varid]
            pvl = varid + "L"
            pvh = varid + "H"
            pvll = varid + "LL"
            pvhh = varid + "HH"
            pvlv = self.store.finaltag[pvl]
            pvhv = self.store.finaltag[pvh]
            pvllv = self.store.finaltag[pvll]
            pvhhv = self.store.finaltag[pvhh]
            if self.name[1] == "T":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                if value < self.ranges[0]:
                    value = self.ranges[0]
                self.Value.setText(f"{value:.1f}")
            if self.name[1] == "L":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                if value < self.ranges[0]:
                    value = self.ranges[0]
                self.Value.setText(f"{value:.1f}")
                if self.name == "4201LI009":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    if value < self.ranges[0]:
                        value = self.ranges[0]
                    self.Value.setText(f"{value:.1f}")
            if self.name[1] == "P":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                if value < self.ranges[0]:
                    value = self.ranges[0]
                self.Value.setText(f"{value:.2f}")
            if self.name[0] == "F":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                if value < self.ranges[0]:
                    value = self.ranges[0]
                self.Value.setText(f"{value:.2f}")
            if self.name[1] == "S":
                if value > self.ranges[1]:
                    value = self.ranges[1]
                if value < self.ranges[0]:
                    value = self.ranges[0]
                self.Value.setText(f"{value:.2f}")
            if self.name[1] == "F":
                if unit == "Nm3/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    if value < self.ranges[0]:
                        value = self.ranges[0]
                    self.Value.setText(f"{value:.3f}")
                elif unit == "kg/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    if value < self.ranges[0]:
                        value = self.ranges[0]
                    self.Value.setText(f"{value:.0f}")
                elif unit == "T/hr":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    if value < self.ranges[0]:
                        value = self.ranges[0]
                    self.Value.setText(f"{value:.1f}")
                elif unit == " ":
                    if value > self.ranges[1]:
                        value = self.ranges[1]
                    if value < self.ranges[0]:
                        value = self.ranges[0]
                    self.Value.setText(f"{value:.2f}")
            # if value > self.ranges[1]:
            #     value = self.ranges[1]
            # elif value < self.ranges[0]:
            #     value = self.ranges[0]
            if value == self.store.SettingDetailsofsensor(varid)[0]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
                self.status.setText("LL")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")
            if value == self.store.SettingDetailsofsensor(varid)[1]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
                self.status.setText("HH")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")
                
            if value < pvlv and value > pvllv:
                self.Value.setStyleSheet("QLabel { color: #FFFF00;font-size:14px;}")
                # QLabel { color: #FF0000; }
                self.status.setText("L")
                self.status.setStyleSheet("QLabel { color: #FFFF00; }")
            elif value <= pvllv and value >= self.store.SettingDetailsofsensor(varid)[0]:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
                self.status.setText("LL")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")
            elif value > pvhv and value < self.store.SettingDetailsofsensor(varid)[3]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
                self.status.setText("H")
                self.status.setStyleSheet("QLabel { color: #FFFF00; }")
            elif value >= pvhhv and value <= pvhv:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
                self.status.setText("HH")
                self.status.setStyleSheet("QLabel { color: #FF0000; }")
            else:
                self.Value.setStyleSheet("color:#40d964; font-size:14px;")
                self.status.setStyleSheet("QLabel { color: black; }")
            
            # if value > self.ranges[1]:
            #     value = self.ranges[1]
            #     self.Value.setText(str(f"{value}"))
            # elif value < self.ranges[0]:
            #     value = self.ranges[0]
            #     self.Value.setText(str(f"{value}"))
            # print(f"{self.variableid}:{value}")
        self.update()



    def changestatus(self,state:bool):
        self.changingrewindstatus.emit(state)

    
    
    @QtCore.pyqtSlot(list)
    def prdstatus(self,status:list):
        self.prdstatussignal.emit(status)
    def SettingValue(self,value):
            if self.itype == "":
                self.Value.setText(str(round(value,2)))
                
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
        QMenu {
            background-color: black;
            color: white;  /* متن آیتم‌ها */
            border: 1px solid #ccc;
        }
        QMenu::item:selected {
            background-color: #505050;
            color: white;  /* رنگ متن هنگام هاور */
        }
    """)
        trend_action = menu.addAction("Show Trend")
        action = menu.exec(event.globalPos())
        if action == trend_action:
            self.trend = Trend(self.variableid,self.itype,self.store,self.ranges)
            self.changingrewindstatus.connect(self.trend.resetTrend)
            self.trend.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Indicator()
    window.show()
    sys.exit(app.exec())
