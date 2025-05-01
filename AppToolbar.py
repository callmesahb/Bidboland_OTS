from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import pyqtSignal,pyqtSlot
import datetime
import os
import subprocess
from APIs import Aspen , AspenSimulatorManager
from Store import Store
import sys

class Toolbar(QtWidgets.QToolBar):
    def __init__(self,store:Store):
        super().__init__()
        self.setWindowTitle("AppToolbar")
        current_dir = os.getcwd()
        self.store = store
        self.icondir = os.path.join(current_dir,"icons")
        self.setMovable(False)
        self.Run = QtGui.QAction("Run",self)
        self.Pause = QtGui.QAction("Pause",self)
        self.Rewind = QtGui.QAction("Rewind",self)
        self.interupt = QtGui.QAction("Interupt",self)
        self.Run.setIcon(QtGui.QIcon(os.path.join(self.icondir,"play.jpg")))
        self.Pause.setIcon(QtGui.QIcon(os.path.join(self.icondir,"Pause.png")))
        self.Rewind.setIcon(QtGui.QIcon(os.path.join(self.icondir,"Rewind.png")))
        self.interupt.setIcon(QtGui.QIcon(os.path.join(self.icondir,"stop.png")))
        self.addAction(self.Run)
        self.addAction(self.Pause)
        self.addAction(self.Rewind)
        self.addAction(self.interupt)
        self.timer = QtWidgets.QLabel("Timer:",self)
        self.addWidget(self.timer)
        self.Run.triggered.connect(self.RunAPI)
        self.Pause.triggered.connect(self.PauseAPI)
        self.Rewind.triggered.connect(self.RewindSim)
        self.store.updatevalues.connect(self.readingdata)
        self.aspen = Aspen()
        
    def RunAPI(self):
        exe_path = r"C:\\BB_403ARegTr_403RegDe_407C2Tr_407C2De\\apis\\Run_Sim.exe"
        try:
            subprocess.Popen(
                [exe_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            print("Cannot open path file")
    def PauseAPI(self):
        self.aspen.PauseSim()
        # exe_path = r"C:\\BB_403ARegTr_403RegDe_407C2Tr_407C2De\\apis\\Pause_Sim.exe"
        # print(exe_path)
        # try:
        #     print("SALAMMM")
        #     subprocess.Popen(
        #         [exe_path],
        #         creationflags=subprocess.CREATE_NO_WINDOW,
        #         stdout=subprocess.DEVNULL,
        #         stderr=subprocess.DEVNULL
        #     )
        # except:
        #     print("Cannot open path file")
    
    def RewindSim(self):
        # exe_path = r"C:\\BB_403ARegTr_403RegDe_407C2Tr_407C2De\\apis\\Rewind_Sim.exe"
        # try:
        #     print("salamm")
        #     subprocess.Popen(
        #         [exe_path]
        #     )
        #     print("Rewind Done")
        # except:
        #     print("Cannot open path file")
        os.startfile(r"C:\\BB_403ARegTr_403RegDe_407C2Tr_407C2De\\apis\\Rewind_Sim.exe")
    
    @pyqtSlot()
    def readingdata(self):
        timerstc = datetime.timedelta(seconds=self.store.finaltag["407EDTIMER"])
        self.timer.setText("Timer:"+str(timerstc))
        
        
def window():
    app = QtWidgets.QApplication(sys.argv)
    win = Toolbar()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()    