
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform
from SDVPlate import Valves
from Store import Store
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
import sys
import os

class valveEV(QWidget):
    ChangingValveStatus = pyqtSignal(int)
    updatevalues = pyqtSignal(dict,list)
    def __init__(self,store:Store, variableid,name, value,rotated):
        super().__init__()
        self.value = value
        self.name = name
        self.rotated = rotated
        self.variableid = variableid
        self.setWindowTitle("valveEV")
        self.faceplate = Valves(store,variableid,value)
        self.store = store
        self.store.updatevalues.connect(self.ReadingValue)
        self.resize(50, 40)
        current_path = os.getcwd()
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
        self.faceplate.ValveChangingPos.connect(self.set_status)

    def load_image(self):
        self.image = {
            "EVg": QPixmap(f"{self.equip_path}/ev2g1.png"),
            "EVr": QPixmap(f"{self.equip_path}/ev2r1.png")
        }
        if self.rotated == "left":
                transform = QTransform().rotate(-90)
                self.image["EVg"] = self.image["EVg"].transformed(transform)
                self.image["EVr"] = self.image["EVr"].transformed(transform)
        if self.rotated == "right":
                transform = QTransform().rotate(90)
                self.image["EVg"] = self.image["EVg"].transformed(transform)
                self.image["EVr"] = self.image["EVr"].transformed(transform)

    @pyqtSlot(int)
    def set_status(self, status):
        match status:
            case 1:
                self.image_label.setPixmap(self.image["EVg"])
                # print("Status set to 1 (green)")
            case 2:
                self.image_label.setPixmap(self.image["EVr"])
                # print("Status set to 2 (red)")
            case _:
                pass
    @pyqtSlot(dict,list)
    def ReadingValue(self,data,tags):
        value = data[self.variableid]
        self.set_status(value)
    #     # print(f"{self.variableid}:{value}")
    #     # self.store.worker.stop()
    #     self.store.timer.stop()
    #     self.updatevalues.emit(data,tags)
        # if not self.store.timer.isActive():
        #     self.store.timer.start(2000)
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.name[2] == "P":
                return
            else:
                self.faceplate.setWindowTitle(self.name)
                self.faceplate.name.setText(self.name)
                self.faceplate.show()
if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = valveEV()
        # window.setStyleSheet("background-color: lightblue;")
        window.show()
        sys.exit(app.exec())
