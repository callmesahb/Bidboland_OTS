from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import pyqtSignal,pyqtSlot
import datetime
import os
import subprocess
from multipletrend import TagPlotWidget
from APIs import Aspen , AspenSimulatorManager
from Store import Store
from SignalBus import SignalBus
import sys

class Toolbar(QtWidgets.QToolBar):
    reset_signal = QtCore.pyqtSignal(bool)
    rewind_triggered = QtCore.pyqtSignal(bool)
    closeallwidgets = QtCore.pyqtSignal(bool)
    starttoplot = QtCore.pyqtSignal(bool)
    def __init__(self,store:Store,tags):
        super().__init__()
        self.setWindowTitle("AppToolbar")
        self.setIconSize(QtCore.QSize(32,32))
        self.setStyleSheet("background-color:#9c938e")
        current_dir = os.getcwd()
        self.store = store
        self.showingsim = False
        self.signalbus = SignalBus()
        self.tags = tags
        self.icondir = os.path.join(current_dir,"icons")
        self.simdir = os.path.join(current_dir,"sim")
        self.setMovable(False)
        self.store.updatevalues.connect(self.checkstatus)
        self.Run = QtGui.QAction("Run",self)
        self.Pause = QtGui.QAction("Pause",self)
        self.Rewind = QtGui.QAction("Rewind",self)
        self.interupt = QtGui.QAction("Interupt",self)
        # self.alarmbar = QtGui.QAction("ALARM",self)
        self.visible = QtWidgets.QPushButton("Visible Simulatiuon",self)
        self.visible.setStyleSheet("font-size:16px;")
        # button = QtWidgets.QToolBar.widgetForAction(self.visible)
        # if button:
        #     button.setStyleSheet("""
        #         background-color: #880000;
        #         color: white;
        #         font-weight: bold;
        #     """)
#         self.setStyleSheet("""
#                            QToolBar {
#         color: white;
#         border: 1px solid gray;
#     }
#     QMenu::item {
#         padding: 8px 24px;
#         background-color: transparent;
#     }
#     QMenu::item:selected {
#         background-color: #0078d7;
#     }
# """)
        self.trend = QtGui.QAction("Trend",self)
        self.Run.setIcon(QtGui.QIcon(os.path.join(self.icondir,"play.jpg")))
        self.Pause.setIcon(QtGui.QIcon(os.path.join(self.icondir,"Pause.png")))
        self.Rewind.setIcon(QtGui.QIcon(os.path.join(self.icondir,"Rewind.png")))
        self.interupt.setIcon(QtGui.QIcon(os.path.join(self.icondir,"stop.png")))
        self.trend.setIcon(QtGui.QIcon(os.path.join(self.icondir,"trend.png")))
        # self.alarmbar.setIcon(QtGui.QIcon(os.path.join(self.icondir,"Flash.png")))
        self.addAction(self.Run)
        self.addAction(self.Pause)
        self.addAction(self.Rewind)
        self.addAction(self.interupt)
        self.addWidget(self.visible)
        self.timerlabel = "Timer:"
        self.runing = False
        self.timer = QtWidgets.QLabel(" " +self.timerlabel,self)
        self.timer.setStyleSheet("font-size:16px;")
        self.Status = QtWidgets.QLabel("  STATUS:")
        self.Status.setStyleSheet("font-size:16px;")
        self.addWidget(self.Status)
        self.timerstatus = QtWidgets.QLabel("  INITIAL  ",self)
        self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:#0400e5;")
        self.addWidget(self.timerstatus)
        
        self.addWidget(self.timer)
        
        self.addAction(self.trend)
        
        
        
        
        # self.addAction(self.alarmbar)
        self.rewind = False
        self.pause = False
        self.Run.triggered.connect(self.RunAPI)
        self.Pause.triggered.connect(self.PauseAPI)
        self.Rewind.triggered.connect(self.RewindSim)
        self.store.updatevalues.connect(self.readingdata)
        self.visible.clicked.connect(self.VisiblingSim)
        self.trend.triggered.connect(self.Showtrend)
        self.interupt.triggered.connect(self.Interupting)
        self.aspen = Aspen(self.simdir)
        self.show_terminate = False


        self.store.updatevalues.connect(self.CheckTIMER)
        # self.store.updatevalues.connect(self.GetSimState)
        
        
      
    def GetSimState(self):
        state = self.aspen.ReadingSimulationState()
        print(state)
    def CheckTIMER(self):
        self.last_message = self.aspen.get_last_message()
        time = self.aspen.GetSimTimer()
        if "terminated" in self.last_message and not self.show_terminate and time > 0.0:
                message = QtWidgets.QMessageBox()
                message.setText("The Unit is Shut Down.\nPlease Perform a Rewind Operation.")
                # message.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
                message.setWindowTitle("ERROR")
                message.exec()
                self.show_terminate = True
        
        
    # def CheckTIMER(self, deltatime):
    #     if not hasattr(self, "start_time"):
    #         print("Start time not set.")
    #         return

    #     current_time = datetime.datetime.now()
    #     elapsed_seconds = (current_time - self.start_time).total_seconds()

    #     opc_timer = int(self.store.finaltag.get("420TIMER", 0))
    #     if opc_timer == 0:
    #         pass
    #     diff = abs(elapsed_seconds - opc_timer)

    #     print(f"Elapsed: {elapsed_seconds:.1f}, OPC: {opc_timer}, Diff: {diff:.1f}")

    #     if diff >= deltatime:
    #         QtWidgets.QMessageBox.warning(
    #             self, "Mismatch Detected",
    #             f"اختلاف زمان بین OPC و زمان واقعی بیشتر از {deltatime} ثانیه است.\nاختلاف: {diff:.1f} ثانیه"
    #         )



    # def CheckTIMER(self):
    #     if not self.start_time:
    #         return  # هنوز اجرا نشده

    #     elapsed_real = (datetime.datetime.now() - self.start_time).total_seconds()

    #     # تا 10 ثانیه اول هیچ کاری نکن
    #     if elapsed_real < 10:
    #         return

    #     if self.timer_error_triggered:
    #         return  # قبلاً ارور داده، دیگه هیچی نگو

    #     opc_timer = int(self.store.finaltag.get("420TIMER", 0))
    #     diff = abs(elapsed_real - opc_timer)

    #     print(f"[TIMER CHECK] Real: {elapsed_real:.1f}s | OPC: {opc_timer}s | Diff: {diff:.1f}s")

    #     if diff >= self.deltatime_threshold:
    #         # یک‌بار هشدار بده و Interrupt کن
    #         self.aspen.interrupt_all(True)
    #         QtWidgets.QMessageBox.critical(
    #             self,
    #             "TIMER Mismatch",
    #             f"اختلاف تایمر با زمان واقعی بیش از {self.deltatime_threshold} ثانیه است.\nSimulation متوقف شد.",
    #         )
    #         self.Interupting()
    #         self.runing = False
    #         self.timer_error_triggered = True

    
    
    
    
    
    def Interupting(self):
        self.aspen.interrupt_all(True)
        self.timerstatus.setText("  STOP  ")
        self.runing = False
        self.starttoplot.emit(True)
        self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:red;")
    def Showtrend(self):
        self.showingtrend = TagPlotWidget(self.store,self.tags)
        self.starttoplot.connect(self.showingtrend.setTimer)
        self.showingtrend.show()
    def RunAPI(self):
        exe_path = r"C:\\BB_U420\\API\\Run_Sim.exe"
        self.timerstatus.setText("  RUN  ")
        self.start_time = datetime.datetime.now()
        self.timer_error_triggered = False
        self.runing = True
        self.rewind = False
        self.starttoplot.emit(True)
        self.show_terminate = False
        # self.store.timer.start(1000)
        # self.timerstatus.setStyleSheet("")
        self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:#5afc56")
        try:
            subprocess.Popen(
                [exe_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            print("Cannot open path file")
        self.rewind_triggered.emit(False)
    
    def PauseAPI(self):
        self.aspen.PauseSim()
        self.pause = True
        self.runing = False
        self.starttoplot.emit(True)
        self.timerstatus.setText("  PAUSE  ")
        # self.timerstatus.setStyleSheet("color:#ffff00")
        self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:#ffff00")
        # exe_path = r"C:\\BB_U420\\apis\\Pause_Sim.exe"
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
        exe_path = r"C:\\BB_U420\\API\\Rewind_Sim.exe"
        self.timerstatus.setText("  REWIND  ")
        self.runing = False
        self.starttoplot.emit(False)
        # self.timerstatus.setStyleSheet("color:#ffff00")
        self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:#0400e5")
        try:
            subprocess.Popen(
                [exe_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            print("Cannot open path file")
        # os.startfile(r"C:\\BB_U420\\apis\\Rewind_Sim.exe")
        self.rewind = True
        print(self.store.history)
        self.store.history.clear()
        self.timer.setText("Timer:00:00:00")
        self.store.settingValueOPC("420TIMER", 0)
        print(self.store.history)
        # self.store.timer.stop()
        self.store.reset_to_initial()
        self.reset_signal.emit(self.rewind)
        self.show_terminate = False
        self.signalbus.reset_all_trends.emit(True)
        self.rewind_triggered.emit(True)
        self.closeallwidgets.emit(True)
    def checkstatus(self):
        if self.timerstatus == "  RUN  ":
            self.store.timer.start(1000)
        elif self.timerstatus == "  PAUSE  ":
            self.store.timer.stop()
        elif self.timerstatus == "  REWIND  ":
            self.store.timer.stop()
        elif self.timerstatus == "  STOP  ":
            self.store.timer.stop()
    # def listingAlarms(self):
    def VisiblingSim(self):
        text = self.visible.text()
        if text[0] == "U":
            self.aspen.Visibling(False)
            self.visible.setText("Visible Simulation")
        if text[0] == "V":
            self.aspen.Visibling(True)
            self.visible.setText("Unvisible Simulation")
    # def VisibleSim(self):
    #     self.aspen.Visibling(True)
    
    @pyqtSlot()
    def readingdata(self):
        timer_value = int(self.store.finaltag["420TIMER"])
        hours, remainder = divmod(timer_value, 3600)
        minutes, seconds = divmod(remainder, 60)
        timestr = f"{hours:02}:{minutes:02}:{seconds:02}"
        if self.runing == True:
            self.timerstatus.setText("  RUN  ")
            self.timerstatus.setStyleSheet("font-size:16px;font-weight:bold;color:#5afc56")
        elif self.rewind and self.runing == False:
            self.timer.setText("Timer:00:00:00")
            self.store.settingValueOPC("420TIMER", 0)
            self.rewind = False
        else:
            self.timer.setText("Timer:" + timestr)
            self.timer.setStyleSheet("font-size:16px;")

        self.update()

        
        
def window():
    app = QtWidgets.QApplication(sys.argv)
    win = Toolbar()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()    