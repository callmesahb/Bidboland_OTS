from PyQt6 import QtWidgets, QtGui, QtCore
import os
from workerThread import Worker
from Store import Store
import json
from MainWindow import MainWindow
import time
from APIs import Aspen

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super().__init__()
        self.rootdir = os.getcwd()
        self.imgdir = os.path.join(self.rootdir,"images")
        self.simdir = os.path.join(self.rootdir,"sim")
        self.datadir = os.path.join(self.rootdir,"data")
        self._initUi()
        self._startThread(self.StartSim,self.SimOpened)
        
    def _initUi(self):
        self.newScale = self._scale()
        self._setImage()
        self.SetFont()
    
    def SetFont(self):
        font = QtGui.QFont("New Times Roman")
        font.setBold(True)
        font.setPixelSize(int(20*self.newScale))
        self.setFont(font)
        
    def _setImage(self):
        self.splshimg = QtGui.QPixmap(
            os.path.join(self.imgdir,"loading_2.jpg"))
        if self.newScale != 1:
            newWidth = int(self.splshimg.size().width() * self.newScale)
            newHeight = int(self.splshimg.size().height() * self.newScale)
            self.splshimg.scaled(newWidth,newHeight)
        self.setPixmap(self.splshimg)
    def _scale(self):
        base_width = 1920
        screen_width =self.screen().size().width()
        scale = screen_width / base_width
        return float(scale)
    
    def Visibling(self):
        Aspen().Visible()
    def _startThread(self,startfnc,endfnc):
        self.worker = Worker(startfnc)
        self.worker.finished.connect(endfnc)
        self.worker.start()
    def StartSim(self):
        self.showMessage("Opening Simulation")
        # self.apis = Aspen()
        # self.apis.Visibling(True)
        # self.showMessage("Simulation Opened")
        pass
    def SimOpened(self):
        self._startThread(self.loadingData,self.DataLoaded)
        
    def loadingData(self):
        self.showMessage("Loading Data...")
        self.data = json.loads(
            open(os.path.join(self.datadir, "data.json"), "r").read())
        self.tags = json.loads(
            open(os.path.join(self.datadir, "tags.json"), "r").read())
    def DataLoaded(self):
        self.showMessage("Data Loaded...")
        self.store = Store(self.data,self.tags)
        self.mainWidget = MainWindow(self.data,self.store)
        self.finish(self.mainWidget)
        self.mainWidget.showMaximized()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    splash = SplashScreen()
    splash.show()
    app.exec()