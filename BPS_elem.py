
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
import sys
from SDVPlate import Valves
import time
import os
import random
from Store import Store


class BPS(QWidget):
        ValveChangingPos = pyqtSignal(int)
        updatevalues = pyqtSignal()
        def __init__(self,store:Store,variableid,name,value,rotated,title):
                super().__init__()
                
                self.resize(50, 40)
                self.value = value
                self.name = name
                self.rotated = rotated
                self.setWindowTitle(name)
                current_path = os.getcwd()
                images = os.path.join(current_path, "images")
                self.equip_path = os.path.join(images, "equipment")

                self.image = {}
                self.load_image()
                self.variableid = variableid
                self.faceplate = Valves(store,variableid,value,title)
                self.faceplate.ValveChangingPos.connect(self.set_status)
                self.store=store
                self.image_label = QLabel(self)
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        
                layout = QVBoxLayout()
                layout.addWidget(self.image_label)
                self.setLayout(layout)
                # repeat_count=10 
                # for i in range(repeat_count):
                #     random_number=random.choice([1,2])
                #     print(f"{random_number}")


                self.set_status(1)  

        @pyqtSlot(int)
        def load_image(self):
                self.image = {
                    "bpsg": QPixmap(os.path.join(self.equip_path,"bpsg.png")),
                    "bpsr": QPixmap(os.path.join(self.equip_path,"bpsr.png"))
                }
                if self.rotated == "left":
                    transform = QTransform().rotate(-90)
                    self.image["bpsg"] = self.image["bpsg"].transformed(transform)
                    self.image["bpsr"] = self.image["bpsr"].transformed(transform)

        def set_status(self, status):
            match status:
                case 1:
                    self.image_label.setPixmap(self.image["bpsg"])
                case 2:
                    self.image_label.setPixmap(self.image["bpsr"])
                case _ :
                        # print("Wrong")
                        pass
        @pyqtSlot()
        def ReadingValue(self):
            value = self.store.finaltag[self.variableid]
            self.set_status(value)
        # def mousePressEvent(self, event:QMouseEvent):
        #     if event.button() == Qt.MouseButton.LeftButton:
        #         self.faceplate.setWindowTitle(self.name)
        #         self.faceplate.name.setText(self.name)
        #         self.faceplate.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = BPS()
        window.setStyleSheet("background-color: lightblue;")
        window.show()
        sys.exit(app.exec())
