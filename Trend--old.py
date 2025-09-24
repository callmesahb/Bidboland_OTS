from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from datetime import datetime
from Store import Store
import sys
import time

class Trend(QtWidgets.QWidget):
    def __init__(self,variableid:str,typelem:str,store:Store):
        super().__init__()
        self.varid = variableid
        self.itype = typelem
        # print(self.varid)
        self.store = store
        self.timestamps = []
        self.spvalues = []
        self.values = []
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.zoom_window = 60
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.info_display = QtWidgets.QLineEdit()
        self.info_display.setReadOnly(True)
        self.setWindowTitle(variableid)
        self._InitUI()
    def _InitUI(self):
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.SettingPlot()
        self.mainlayout.addWidget(self.plotwidget)
        self.mainlayout.addWidget(self.info_display)
        self.setLayout(self.mainlayout)
    
    def SettingPlot(self):
        axis = pg.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        self.plotwidget = pg.PlotWidget(axisItems={'bottom': axis})
        self.plotwidget.setYRange(0,100)
        self.plotwidget.setMouseEnabled(x=False,y=True)
        if self.itype == "controller":
            self.plotwidget.addLegend()
            self.curve = self.plotwidget.plot(pen='g', name="PV")
            self.sp_curve = self.plotwidget.plot(pen='r', name="SP")
        elif self.itype == "":
            self.curve = self.plotwidget.plot(pen='g',name="PV")
        self.plotwidget.setLabel('left', 'Value')
        self.plotwidget.showGrid(x=False, y=True)
        
    def update(self):
        try:
            global raw_value
            # raw_value = self.store.finaltag[self.varid]
                # raw_value = self.store.finaltag[]
            if self.itype == "controller":
                pvname = self.varid + "PV"
                spname = self.varid + "SP"
                raw_value = self.store.finaltag[pvname]
                raw_sp = self.store.finaltag[spname]
                min_r = self.store.SettingDetailsofsensor(pvname)[0]
                max_r = self.store.SettingDetailsofsensor(pvname)[1]
                scaled_value = ((raw_value - min_r) / (max_r - min_r)) * 100
                scaled_value = max(0, min(100, scaled_value))
                scaled_sp = ((raw_sp - min_r) / (max_r - min_r)) * 100
                scaled_sp = max(0, min(100, scaled_sp))
            else:
                raw_value = self.store.finaltag[self.varid]
                min_r = self.store.SettingDetailsofsensor(self.varid)[0]
                max_r = self.store.SettingDetailsofsensor(self.varid)[1]
                scaled_value = ((raw_value - min_r) / (max_r - min_r)) * 100
                scaled_value = max(0, min(100, scaled_value))
            now = time.time()

            # min_r = self.store.SettingDetailsofsensor(self.varid)[0]
            # max_r = self.store.SettingDetailsofsensor(self.varid)[1]
            # scaled_value = ((raw_value - min_r) / (max_r - min_r)) * 100
            # scaled_value = max(0, min(100, scaled_value))

            print(f"{datetime.fromtimestamp(now).strftime('%H:%M:%S')} | مقدار اصلی: {raw_value} | مقیاس‌شده: {scaled_value:.2f}%")

            self.timestamps.append(now)
            self.values.append(raw_value)
            if self.itype == "controller":
                self.spvalues.append(raw_sp)

            while self.timestamps and self.timestamps[0] < now - 600:
                self.timestamps.pop(0)
                self.values.pop(0)
                if self.itype == "controller":
                    self.spvalues.pop(0)

            if self.values:
                all_values = self.values[:]
                if self.itype == "controller":
                    all_values += self.spvalues  # SP رو هم اضافه کن به مقادیر
                
                min_y = min(all_values)
                max_y = max(all_values)

                # اختلاف زیاد یا خارج شدن از محدوده → Y-range رو تنظیم کن
                margin = 5
                if abs(max_y - min_y) > 5:  # یعنی تغییر زیادی بوده
                    self.plotwidget.setYRange(min_y - margin, max_y + margin)

            self.plotwidget.setXRange(now - self.zoom_window, now)
            self.curve.setData(self.timestamps, self.values)
            if self.itype == "controller":
                self.sp_curve.setData(self.timestamps, self.spvalues)
            self.info_display.setText(f"{datetime.fromtimestamp(now).strftime('%H:%M:%S')}:{raw_value}")
            
        except Exception as e:
            print(e)
            
def win():
    app = QtWidgets.QApplication(sys.argv)
    win = Trend()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    win()