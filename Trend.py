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
        print(self.varid)
        self.itype = typelem
        self.store = store
        self.timestamps = []
        self.values = []
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
        self.curve = self.plotwidget.plot(pen='g')
        self.plotwidget.setLabel('left', 'Value(%)')
        self.plotwidget.showGrid(x=False, y=True)
        
    def update(self):
        try:
            global raw_value
            raw_value = self.store.finaltag[self.varid]
            now = time.time()

            min_r = self.store.SettingDetailsofsensor(self.varid)[0]
            max_r = self.store.SettingDetailsofsensor(self.varid)[1]
            scaled_value = ((raw_value - min_r) / (max_r - min_r)) * 100
            scaled_value = max(0, min(100, scaled_value))

            print(f"{datetime.fromtimestamp(now).strftime('%H:%M:%S')} | مقدار اصلی: {raw_value} | مقیاس‌شده: {scaled_value:.2f}%")

            self.timestamps.append(now)
            self.values.append(scaled_value)

            while self.timestamps and self.timestamps[0] < now - 600:
                self.timestamps.pop(0)
                self.values.pop(0)

            if self.values:
                min_y = min(self.values)
                max_y = max(self.values)
                self.plotwidget.setYRange(min_y - 5, max_y + 5)

            self.plotwidget.setXRange(now - self.zoom_window, now)
            self.curve.setData(self.timestamps, self.values)
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