
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from ControllerPlate import ControllerPlate
from Store import Store
import sys
import time
import os
import random

class HAND(QWidget):
        changeHandtype = pyqtSignal(str)
        def __init__(self,store:Store,varid):
                super().__init__()
                self.setWindowTitle("HAND")
                self.store = store
                self.varid = varid
                self.resize(50, 40)
                current = os.getcwd()
                path = os.path.join(current,"images")
                self.eqpath = os.path.join(path,"equipment")
                self.list = self.store.GettingControllerDetails(varid)
                self.plate = ControllerPlate(varid,self.list,varid,store)
                # self.plate.changeHandtype.connect(self.set_status)

                self.image = {}
                self.load_image()

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


        def load_image(self):
                self.image = {
                    "ha": QPixmap(os.path.join(self.eqpath,"h2.png")),
                    "hm": QPixmap(os.path.join(self.eqpath,"h2y.png")),
                }
        @pyqtSlot(str)
        def set_status(self, status):
            match status:
                case 0:
                    self.image_label.setPixmap(self.image["ha"])
                case 1:
                    self.image_label.setPixmap(self.image["hm"])
                case _ :
                        print("Wrong")
                        
        @pyqtSlot()
        def ReadingValue(self):
            tv = self.varid + "TV"
            tvvalue = self.store.finaltag[tv]
            self.set_status(tvvalue)
       

if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = HAND()
        # window.setStyleSheet("background-color: lightblue;")
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)  
        window.show()
        sys.exit(app.exec())
