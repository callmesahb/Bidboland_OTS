
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PumpFacePlate import PumpFacePlate
import sys
import os
from Store import Store 



class Aircooler(QWidget):
    PumpChangingPos = pyqtSignal(str)
    updatevalues = pyqtSignal()
    def __init__(self,store:Store,variableid,name,value,title):
        super().__init__()
        self.setWindowTitle("Aircooler")
        self.value=value
        self.resize(50, 40)
        self.name = name
        self.variableid=variableid
        self.store=store
        self.title = title
        current_path = os.getcwd()
        images = os.path.join(current_path, "images")
        self.equip_path = os.path.join(images, "equipment")

        self.image = {}
        self.load_image()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # self.faceplate.PumpChangingPos.connect(self.set_status)
        self.store.updatevalues.connect(self.ReadingValue)
  
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

   
        self.set_status(value)

    def load_image(self):
        self.image = {
            "Ag": QPixmap(os.path.join(self.equip_path,"AirCoolerg.png")),
            "Ar": QPixmap(os.path.join(self.equip_path,"AirCoolerr.png")),
        }

    @pyqtSlot(int)
    def set_status(self, status):
        if status == 1:
            self.image_label.setPixmap(self.image["Ag"])
        elif status == 2:
            self.image_label.setPixmap(self.image["Ar"])
    @pyqtSlot()
    def ReadingValue(self):
        value = self.store.finaltag[self.variableid]
        self.set_status(value)
    
            
    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            print(self.variableid)
            self.faceplate = PumpFacePlate(self.variableid,self.store,self.title)
            self.faceplate.setWindowTitle(self.name)
            self.faceplate.pname.setText(self.name)
            self.faceplate.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Aircooler()
    window.show()
    sys.exit(app.exec())