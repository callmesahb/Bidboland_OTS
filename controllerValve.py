
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QTransform,QMouseEvent , QPainter
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from ControllerPlate import ControllerPlate
import sys
import os
import numpy as np
from Store import Store

class ControllerValve(QWidget):
        ChangePosValve = pyqtSignal(float)
        updatevalues = pyqtSignal()
        def __init__(self,name,rotated,pvvalues,variableid:str,store:Store):
                super().__init__()
                self.setWindowTitle("controllerValve")
                self.resize(50, 40)
                self.faceplates = []
                self.rotated = rotated
                self.name = name
                self.pvvalues = pvvalues
                self.variableid = variableid
                current_path = os.getcwd()
                images = os.path.join(current_path, "images")
                self.equip_path = os.path.join(images, "equipment")
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                self.image = {}
                self.faceplate = ControllerPlate(name,pvvalues,variableid,store)
                self.load_image()

                self.image_label = QLabel(self)
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                self.faceplate.ChangePosValve.connect(self.set_status)
                layout = QVBoxLayout()
                layout.addWidget(self.image_label)
                self.setLayout(layout)
                self.load_image()
                # store.updatevalues.connect(self.settingValueController)
                # repeat_count=10 
                # for i in range(repeat_count):
                #     random_number=random.choice([1,2])
                #     print(f"{random_number}")
                self.store=store

                # self.set_status(5)
                
                
                
        def load_image(self):
            self.image = {
                "Controller_r": QPixmap(f"{self.equip_path}/cont2r.png"),
                "Controller_g": QPixmap(f"{self.equip_path}/contg2.png")
            }

            if self.rotated == "left":
                transform = QTransform().rotate(-90)
                self.image["Controller_g"] = self.image["Controller_g"].transformed(transform)
                self.image["Controller_r"] = self.image["Controller_r"].transformed(transform)
            if self.rotated == "right":
                transform = QTransform().rotate(90)
                self.image["Controller_g"] = self.image["Controller_g"].transformed(transform)
                self.image["Controller_r"] = self.image["Controller_r"].transformed(transform)
        # def paintEvent(self, event):
        #     painter = QPainter(self)
        #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        #     # painter.translate(self.width() / 2, self.height() / 2)
        #     # painter.rotate(90)
        #     # painter.translate(-self.height() / 2, -self.width() / 2)
        #     painter.drawPixmap(0, 0, self.image1)     
        def set_status(self, status):
            match status:
                case x if -1000 <= x < 1:
                    self.image_label.setPixmap(self.image["Controller_r"])
                case x if 1 <= x <= 100:
                    self.image_label.setPixmap(self.image["Controller_g"])
                case _:
                    pass
            self.update()
                
        @pyqtSlot()
        def settingValueController(self):
            value =self.store.finaltag[self.variableid]
            self.set_status(value)
            # print(value)
                    
        def mousePressEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                if not hasattr(self, 'faceplate') or self.faceplate is None or not self.faceplate.isVisible():
                    varid = self.variableid[:-2]
                    self.faceplate = ControllerPlate(self.name, self.pvvalues, varid, self.store)
                    self.faceplate.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
                    self.faceplate.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
                    self.faceplate.destroyed.connect(self._faceplate_closed)
                    self.faceplate.show()
                else:
                    self.faceplate.raise_()
                    self.faceplate.activateWindow()

            return super().mousePressEvent(event)

        def _faceplate_closed(self):
            self.faceplate = None


        
        def Updatingvalue(self,data):
            self.value = data.get(self.variableid,self.value)
            self.update()

                        
         

             
if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = ControllerValve("0LIC","left")
        window.show()
        sys.exit(app.exec())