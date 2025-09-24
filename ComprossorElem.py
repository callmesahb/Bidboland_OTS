
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform , QPainter
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
import os
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from Store import Store
from SDVPlate import Valves



class Comprossor(QWidget):
    ChangingValveStatus = pyqtSignal(int)
    def __init__(self,store:Store, variableid,name, value,title ):
        super().__init__()
        self.value = value
        self.name = name
        self.variableid = variableid
        self.title = title
        self.setWindowTitle("Comprossor")
        self.faceplate = Valves(store,variableid,value,title)
        self.resize(50, 40)
        current_path = os.getcwd()
        images = os.path.join(current_path, "images")
        self.equip_path = os.path.join(images, "equipment")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.image = {}
        self.load_image()
        self.store = store
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

  
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.set_status(value)
        self.faceplate.ValveChangingPos.connect(self.set_status)

    def load_image(self):
        self.image = {
            "Cg": QPixmap(os.path.join(self.equip_path,"comprossorg.png")),
            "Cr": QPixmap(os.path.join(self.equip_path,"comprossorr.png"))
        }
    @pyqtSlot(int)
    def set_status(self, status):
        match status:
            case 1:
                self.image_label.setPixmap(self.image["Cg"])
            case 2:
                self.image_label.setPixmap(self.image["Cr"])   
        self.update() 
    def ReadingValue(self):
        value = self.store.finaltag[self.variableid]
        self.set_status(value)
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # self.faceplate.name.setText(self.name)
            self.faceplate.show()
        return super().mousePressEvent(event)


if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = Comprossor()
        # window.setStyleSheet("background-color: lightblue;")
        window.show()
        sys.exit(app.exec())