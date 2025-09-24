
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PumpFacePlate import PumpFacePlate
import sys
import os
import time
import random
from Store import Store

class NormalPumpLG(QWidget):
        PumpChangingPos = pyqtSignal(str)
        updatevalues = pyqtSignal()
        def __init__(self,store:Store,variableid,name,title):
            super().__init__()
            self.name = name
            self.store=store
            self.variableid=variableid
            varid = self.variableid + "LG"
            # self.setWindowTitle(name)
            

            current_path = os.getcwd()
            self.faceplate = PumpFacePlate(variableid,store,title)
            self.store.updatevalues.connect(self.faceplate.ReadValue)
            # self.faceplate.PumpChangingPos.connect(self.set_status)
            images = os.path.join(current_path, "images")
            self.fvalue = self.store.finaltag[varid]
            self.equip_path = os.path.join(images, "equipment")
            
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            self.image = {}
            # self.load_image()

            self.image_label = QLabel(self)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    
            layout = QVBoxLayout()
            layout.addWidget(self.image_label)
            self.setLayout(layout)

            self.RIGHT="right"
            self.LEFT="left"
            self.store.updatevalues.connect(self.ReadingValue)
            self.set_status("RUN")
                          


        def load_image(self):
                self.image = {
                    "lalalap1": QPixmap(os.path.join(self.equip_path,"lalalap1.png")),
                }

                          
        @pyqtSlot()
        def set_status(self,status):
                match status:
                    case 2:
                        self.image_label.setPixmap(self.image["lalalap1"])
        @pyqtSlot()
        def ReadingValue(self):
            varid = self.variableid + "LG"
            value = self.store.finaltag[varid]
            # print(f"{varid}:{value}:{self.fvalue}")
            if value == self.fvalue:
                self.setWindowOpacity(0.0)
            elif value != self.fvalue:
                self.setWindowOpacity(1.0)
                if value == 2:
                    self.store.settingValueOPC(self.variableid,2)
                elif value == 1:
                    self.store.settingValueOPC(self.variableid,1)
                self.setStyleSheet("""
                QWidget {
                    background: #676767;
                    border: 2px solid #ff0000;
                    border-radius: 3px;
                }
            """)
            self.update()
        # def mousePressEvent(self, event:QMouseEvent):
        #     if event.button() == Qt.MouseButton.LeftButton:
        #         if len(self.name) == 6:
        #             pass
        #         else:
        #             self.faceplate.setWindowTitle(self.name)
        #             self.faceplate.show()
                
        

if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = NormalPumpLG()
        # window.setStyleSheet("background-color: lightblue;")
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # پس‌زمینه کاملاً شفاف
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # حذف فریم پنجره
        window.show()
        sys.exit(app.exec())
