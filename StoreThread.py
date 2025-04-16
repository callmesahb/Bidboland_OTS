from PyQt6 import QtCore
import time

class StoreThread(QtCore.QThread):
    data_ready = QtCore.pyqtSignal(dict,list)
    
    def __init__(self,opc,csvfile,tag,parent = None):
        super().__init__(parent)
        self.opc = opc
        self.csvfile = csvfile
        self.tag = tag
        self.running = True
        self.newtags = {i: self.opc.getValue(i) for i in self.csvfile["tag"]}
        self.finaltag = self.newtags
        # self.setAutoDelete(True)
        
        
    def run(self):
        while self.running:
            newtags = {i: self.opc.getValue(i) for i in self.csvfile["tag"]}
            self.finaltag = newtags
            # print("Runningggg")
            # time.sleep(0.5)
        
    def stop(self):
        self.running = False