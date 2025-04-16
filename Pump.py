
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PumpFacePlate import PumpFacePlate
import sys
import os
import time
import random
from Store import Store

class NormalPump(QWidget):
        PumpChangingPos = pyqtSignal(str)
        updatevalues = pyqtSignal()
        def __init__(self,store:Store,variableid,name,value,rotated):
            super().__init__()
            self.name = name
            self.value = value
            self.store=store
            self.variableid=variableid
            self.rotated = rotated
            # self.setWindowTitle(name)
            
            self.resize(50, 40)
            current_path = os.getcwd()
            self.faceplate = PumpFacePlate(variableid,store)
            # self.faceplate.PumpChangingPos.connect(self.set_status)
            images = os.path.join(current_path, "images")
            self.equip_path = os.path.join(images, "equipment")
            
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            self.image = {}
            self.load_image()

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
                    "p1g": QPixmap(os.path.join(self.equip_path,"p1.png")),
                    "p1r": QPixmap(os.path.join(self.equip_path,"p1r.png"))
                }
                if self.rotated == "left":
                    transform = QTransform().rotate(180)
                    self.image["p1g"] = self.image["p1g"].transformed(transform)
                    self.image["p1r"] = self.image["p1r"].transformed(transform)

                          
        @pyqtSlot()
        def set_status(self,status):
                match status:
                    case 1:
                        self.image_label.setPixmap(self.image["p1g"])
                    case 2:
                        self.image_label.setPixmap(self.image["p1r"])
        @pyqtSlot()
        def ReadingValue(self):
            value = self.store.finaltag[self.variableid]
            self.set_status(value)
        def mousePressEvent(self, event:QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                self.faceplate.setWindowTitle(self.name)
                self.faceplate.pname.setText(self.name)
                self.faceplate.show()
                
        

if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = NormalPump()
        # window.setStyleSheet("background-color: lightblue;")
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # پس‌زمینه کاملاً شفاف
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # حذف فریم پنجره
        window.show()
        sys.exit(app.exec())
