
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QTransform,QMouseEvent , QPainter
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from ControllerPlate import ControllerPlate
import sys
import os
import numpy as np
from Store import Store

class ControllerLogic(QWidget):
        ChangePosValve = pyqtSignal(float)
        updatevalues = pyqtSignal()
        def __init__(self,name,store:Store,rotated):
                super().__init__()
                self.setObjectName("controller")
                self.setWindowTitle("controllerValve")
                # self.resize(50, 40)
                self.faceplates = []
                self.name = name
                self.rotated = rotated
                current_path = os.getcwd()
                images = os.path.join(current_path, "images")
                self.equip_path = os.path.join(images, "equipment")
                self.image_label = QLabel(self)
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.allrightnames = ["1LIC029B"]
        
                layout = QVBoxLayout()
                layout.addWidget(self.image_label)
                self.setLayout(layout)
                self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
                self.store=store
                varid = self.name + "LG"
                self.fvalue = self.store.finaltag[varid]
                self.store.updatevalues.connect(self.ReadingValue)

        def ChangeStyle(self):
            if self.name in self.allrightnames:
                w = 73
                h = 51
            else:
                w = 50
                h = 87
            return w,h
        def _faceplate_closed(self):
            self.faceplate = None


        
        def Updatingvalue(self,data):
            self.value = data.get(self.variableid,self.value)
            self.update()


        @pyqtSlot()
        def ReadingValue(self):
            varid = self.name + "LG"
            value = self.store.finaltag[varid]
            
            if value == 1:
                self.setWindowOpacity(0.0)
            elif value == 2:
                self.setWindowOpacity(1.0)
                self.setStyleSheet("""
                QWidget {
                    background: #676767;
                    border: 2px solid #ff0000;
                    border-radius: 2px;
                }
            """)
            self.update()   
if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = ControllerLogic("0LIC","left")
        window.show()
        sys.exit(app.exec())