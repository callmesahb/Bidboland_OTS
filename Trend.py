from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from datetime import datetime
from Store import Store
from SignalBus import SignalBus
import sys
import time

class Trend(QtWidgets.QWidget):
    def __init__(self,variableid:str,typelem:str,store:Store,ranges):
        super().__init__()
        self.varid = variableid
        self.itype = typelem
        self.ranges = ranges
        # print(self.varid)
        self.store = store
        self.trend_enabled = True
        self.timestamps = []
        self.spvalues = []
        self.opvalues = []
        self.values = []
        self.signalbus = SignalBus()
        self.signalbus.reset_all_trends.connect(self.resetTrend)
        self.showyelem = ''
        self.showyunit = ''
        self.showy = ''
        self.unit = ""
        if typelem == "":
            self.unit = self.store.GettingUnit(variableid)
        elif typelem == "controller":
            varid = variableid + "PV"
            self.unit = self.store.GettingUnit(varid)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.zoom_window = 600
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTrend)
        self.timer.start(1000)
        # self.store.updatevalues.connect(self.updateTrend)
        self.info_display = QtWidgets.QLineEdit()
        self.info_display.setReadOnly(True)
        self.setWindowTitle("Trend")
        if variableid[4] == "T":
            self.showyunit = "C"
            self.showyelem = "Temperature"
            self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
        elif variableid[4] == "P":
            if variableid[4] == "P" and variableid[5] == "D":
                self.showyunit = "bard"
                self.showyelem = "Pressure"
                self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
            else:
                self.showyunit = "barg"
                self.showyelem = "Pressure"
                self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
        elif variableid[4] == "L":
            self.showyunit = "%"
            self.showyelem = "Level"
            self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
        
        elif variableid[4] == "F":
            self.showyunit = f"{self.unit}"
            self.showyelem = f"Flow"
            self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
            
        elif variableid[4] == "A":
            self.showyunit = "PPMV"
            self.showyelem = "Analyzer"
            self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
        elif variableid[4] == "P" and len(variableid) == 10:
            self.showyunit = "bard"
            self.showyelem = "Pressure"
            self.showy = f'{self.showyelem}' + f' ({self.showyunit})'
        self._InitUI()
    def _InitUI(self):
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.SettingPlot()
        self.mainlayout.addWidget(self.plotwidget)
        self.mainlayout.addWidget(self.info_display)
        self.setLayout(self.mainlayout)
    
    
    def resetTrend(self, status: bool):
        if status:
            self.trend_enabled = False
            # self.timer.stop()
            try:
                if self.itype == "controller":
                    self.timer.stop()
                    self.spvalues.clear()
                    self.opvalues.clear()
                    self.values.clear()
                    self.curve.setData([], [])
                    self.sp_curve.setData([], [])
                    # self.op_curve.setData([], [])
                    self.info_display.clear()
                elif self.itype == "chtrend":
                    self.timer.stop()
                    self.spvalues.clear()
                    self.opvalues.clear()
                    self.values.clear()
                    self.curve.setData([], [])
                    # self.sp_curve.setData([], [])
                    self.op_curve.setData([], [])
                    self.info_display.clear()
                else:
                    self.timer.stop()
                    self.values.clear()
                    self.curve.setData([], [])
                    self.info_display.clear()

            except Exception as e:
                print(f"Error during resetTrend (type={self.itype}):", e)
        else:
            self.trend_enabled = True  # فعال کردن دوباره
            self.timer.start(1000)
            self.updateTrend()
            
        self.update()

    
    
    def SettingPlot(self):
        # axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        x_axis = pg.AxisItem(orientation='bottom')
        self.plotwidget = pg.PlotWidget(axisItems={'bottom': x_axis})
        self.plotwidget.setMouseEnabled(x=False,y=True)
        if self.itype == "controller":
            self.plotwidget.addLegend()
            self.curve = self.plotwidget.plot(pen='g', name=f"{self.varid}PV")
            self.sp_curve = self.plotwidget.plot(pen='r', name=f"{self.varid}SP")
            self.plotwidget.setYRange(self.ranges[0],self.ranges[1])
            self.plotwidget.setLabel('left', self.showy)
        if self.itype == "chtrend":
            self.plotwidget.addLegend()
            self.showyunit = "(%)"
            self.plotwidget.setYRange(0,100)
            self.showy = f'{self.showyelem}' + f'{self.showyunit}'
            self.curve = self.plotwidget.plot(pen='g', name=f"{self.varid}PV")
            self.op_curve = self.plotwidget.plot(pen='b', name=f"{self.varid}OP")
            self.plotwidget.setLabel('left', f"{self.showy}")
            
        elif self.itype == "":
            self.plotwidget.addLegend()
            self.plotwidget.setYRange(self.ranges[0],self.ranges[1])
            self.plotwidget.setLabel('left', self.showy)
            self.curve = self.plotwidget.plot(pen='g',name=f"{self.varid}PV")
        self.plotwidget.showGrid(x=False, y=True)


    def updateTrend(self):
        if not self.trend_enabled:
            return
        try:
            global raw_value
            now = self.store.finaltag.get("420TIMER", 0)

            if now <= 0:
                return  # از رسم جلوگیری کن

            if self.itype == "controller":
                pvname = self.varid + "PV"
                spname = self.varid + "SP"

                if not self.timestamps:
                    spdata = self.store.history.get(spname, [])
                    pvdata = self.store.history.get(pvname, [])
                    if pvdata and spdata:
                        self.timestamps = [item[0] for item in pvdata if item[0] > 0]
                        self.values = [item[1] for item in pvdata if item[0] > 0]
                        self.spvalues = [item[1] for item in spdata if item[0] > 0]

                raw_value = self.store.finaltag.get(pvname, 0)
                raw_sp = self.store.finaltag.get(spname, 0)

                self.timestamps.append(now)
                self.values.append(raw_value)
                self.spvalues.append(raw_sp)

                while self.timestamps and self.timestamps[0] < now - 300:
                    self.timestamps.pop(0)
                    self.values.pop(0)
                    self.spvalues.pop(0)

                if len(self.timestamps) == len(self.spvalues):
                    self.sp_curve.setData(self.timestamps, self.spvalues)
                    self.curve.setData(self.timestamps, self.values)

            elif self.itype == "chtrend":
                pvname = self.varid + "PVs"
                opname = self.varid + "OP"

                if not self.timestamps:
                    opdata = self.store.history.get(opname, [])
                    pvdata = self.store.history.get(pvname, [])
                    if pvdata and opdata:
                        self.timestamps = [item[0] for item in pvdata if item[0] > 0]
                        self.values = [item[1] for item in pvdata if item[0] > 0]
                        self.opvalues = [item[1] for item in opdata if item[0] > 0]

                raw_value = self.store.finaltag.get(pvname, 0)
                raw_op = self.store.finaltag.get(opname, 0)

                self.timestamps.append(now)
                self.values.append(raw_value)
                self.opvalues.append(raw_op)

                while self.timestamps and self.timestamps[0] < now - 300:
                    self.timestamps.pop(0)
                    self.values.pop(0)
                    self.opvalues.pop(0)

                if len(self.timestamps) == len(self.opvalues):
                    self.op_curve.setData(self.timestamps, self.opvalues)
                    self.curve.setData(self.timestamps, self.values)

            else:
                if not self.timestamps:
                    data = self.store.history.get(self.varid, [])
                    if data:
                        self.timestamps = [item[0] for item in data if item[0] > 0]
                        self.values = [item[1] for item in data if item[0] > 0]

                raw_value = self.store.finaltag.get(self.varid, 0)

                self.timestamps.append(now)
                self.values.append(raw_value)

                while self.timestamps and self.timestamps[0] < now - 300:
                    self.timestamps.pop(0)
                    self.values.pop(0)

                self.curve.setData(self.timestamps, self.values)

            # if now >= self.zoom_window:
            #     self.plotwidget.setXRange(now - self.zoom_window, now)
            # else:
            #     self.plotwidget.setXRange(0, self.zoom_window)

            self.info_display.setText(f"{now} : {raw_value}")

            if self.itype == "chtrend":
                self.info_display.setHidden(True)

        except Exception as e:
            print(f"Error in updateTrend: {e}")

            
def win():
    app = QtWidgets.QApplication(sys.argv)
    win = Trend()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    win()