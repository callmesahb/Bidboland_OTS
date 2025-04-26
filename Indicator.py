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
    
    def __init__(self,name,value,itype,pvvalues,store:Store,variableid):
        super().__init__()
        self.setStyleSheet("background-color:black")
        self.name = name
        self.value = value
        self.itype = itype
        self.pvvalues = pvvalues
        self.store = store
        self.variableid = variableid
        self.InitUI()
        
        
    def InitUI(self):
        self.hlayout = QtWidgets.QHBoxLayout()
        
        
        self.setMinimumHeight(5)
        
        self.settingValue()
    def settingValue(self):
        self.Value = QtWidgets.QLabel("245",self)
        self.Value.move(8,0)
        if self.itype == "":
            self.Value.setText(str(round(self.value,2)))
        if self.itype == "controller":
            self.Value.setText(str(round(self.pvvalues[1],2)))
        self.Value.setStyleSheet("color:#40d964; font-size:14px;")
        
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.itype == "controller":
                self.contplate = ControllerPlate(self.name,self.pvvalues,self.variableid,self.store)
                self.contplate.show()
            if self.itype == "":
                self.sensor = Sensor(self.value,self.store,self.name,self.variableid)
                self.sensor.setWindowTitle(self.name)
                self.sensor.sensorname.setText(self.name)
                self.sensor.show()
    
    @QtCore.pyqtSlot()
    def updatinvalue(self):
        if self.itype == "":
            value = self.store.finaltag[self.variableid]
            self.Value.setText(str(round(value,2)))
            if value < self.store.SettingDetailsofsensor(self.variableid)[4] and value > self.store.SettingDetailsofsensor(self.variableid)[2]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
            elif value < self.store.SettingDetailsofsensor(self.variableid)[2]:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
            elif value > self.store.SettingDetailsofsensor(self.variableid)[5] and value < self.store.SettingDetailsofsensor(self.variableid)[3]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
            elif value > self.store.SettingDetailsofsensor(self.variableid)[3]:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
            else:
                self.Value.setStyleSheet("color:#40d964; font-size:14px;")
        if self.itype == "controller":
            varid = self.variableid + "PV"
            value = self.store.finaltag[varid]
            self.Value.setText(str(round(value,2)))
            if value < self.store.SettingDetailsofsensor(varid)[4] and value > self.store.SettingDetailsofsensor(varid)[2]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
            elif value < self.store.SettingDetailsofsensor(varid)[2]:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
            elif value > self.store.SettingDetailsofsensor(varid)[5] and value < self.store.SettingDetailsofsensor(varid)[3]:
                self.Value.setStyleSheet("color:#FFFF00; font-size:14px;")
            elif value > self.store.SettingDetailsofsensor(varid)[3]:
                self.Value.setStyleSheet("color:#FF0000; font-size:14px;")
            else:
                self.Value.setStyleSheet("color:#40d964; font-size:14px;")
            # print(f"{self.variableid}:{value}")
    
    def SettingValue(self,value):
            if self.itype == "":
                self.Value.setText(str(round(value,2)))
                
    # def contextMenuEvent(self, event):
    #     menu = QtWidgets.QMenu(self)
    #     trend_action = menu.addAction("Show Trend")
    #     action = menu.exec(event.globalPos())
    #     if action == trend_action:
    #         self.trend = Trend(self.variableid,self.itype,self.store)
    #         self.trend.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Indicator()
    window.show()
    sys.exit(app.exec())
