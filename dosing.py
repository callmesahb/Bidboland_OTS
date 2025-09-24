
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QTransform,QMouseEvent
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PumpFacePlate import PumpFacePlate
import sys
import time
import os
import random
from Store import Store

class DosingPump(QWidget):
        PumpChangingPos = pyqtSignal(str)
        updatevalues = pyqtSignal()
        def __init__(self, store:Store,variableid ,value,rotated,title):
                super().__init__()
                self.setWindowTitle("p2")
                self.rotated = rotated
                
                self.resize(50, 40)
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
                
                current_path = os.getcwd()
                images = os.path.join(current_path, "images")
                self.equip_path = os.path.join(images, "equipment")
                self.store=store
                self.variableid=variableid
                self.value=value
                self.title = title
                self.faceplate = PumpFacePlate(variableid,store,title)
                # self.faceplate.PumpChangingPos.connect(self.set_status)
                self.store.updatevalues.connect(self.ReadingValue)

                self.image = {}
                self.load_image()

                self.image_label = QLabel(self)
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
                layout = QVBoxLayout()
                layout.addWidget(self.image_label)
                self.setLayout(layout)

                self.RIGHT="right"
                self.LEFT="left"
                self.UP="up"
                self.DOWN="down"

                self.set_status(value)

                          


        def load_image(self):
                self.image = {
                    "p2gl": QPixmap(f"{self.equip_path}/p2gl.png"),
                    "p2rl": QPixmap(f"{self.equip_path}/p2rl.png")
                }
                if self.rotated == "up":
                    transform = QTransform().rotate(90)
                    self.image["p2gl"] = self.image["p2gl"].transformed(transform)
                    self.image["p2rl"] = self.image["p2rl"].transformed(transform)
                else:
                    self.image["p2gl"] = self.image["p2gl"]
                    self.image["p2rl"] = self.image["p2rl"]

                          
        @pyqtSlot(int)
        def set_status(self,status:str):
            match status:
                case 1:
                    self.image_label.setPixmap(self.image["p2gl"])
                case 2:
                    self.image_label.setPixmap(self.image["p2rl"])
        
                        
        def mousePressEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                self.faceplate.show()
            return super().mousePressEvent(event)
        @pyqtSlot()
        def ReadingValue(self):
            value = self.store.finaltag[self.variableid]
            self.set_status(value)

if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = DosingPump("left")
        # window.setStyleSheet("background-color: lightblue;")
        
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # حذف فریم پنجره
        window.show()
        sys.exit(app.exec())
