
from PyQt6.QtWidgets import QLabel, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PyQt6 import QtWidgets
import sys
import time
import random
import os
from Store import Store
class Filter(QWidget):
    updatevalues = pyqtSignal()
    def __init__(self, store:Store, variableid,name,value):
        super().__init__()
        self.setWindowTitle("filter")
        current_path = os.getcwd()
        images = os.path.join(current_path, "images")
        self.equip_path = os.path.join(images, "equipment")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.name = name
        self.value = value
        self.store=store
        self.variableid=variableid
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(os.path.join(self.equip_path,"filter.png")))
        self.label.setScaledContents(True)
        
        self.checkBoxf = QtWidgets.QCheckBox(self)
        self.checkBoxf.stateChanged.connect(self.changingvalue)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkBoxf)
        self.setLayout(layout)
        self.store.updatevalues.connect(self.settingValueController)
        
        
    def toggle_images(self ,state):
        if state==1:
            self.label.setPixmap(QPixmap(os.path.join(self.equip_path,"filter.png")))
            self.checkBoxf.setChecked(True)
        elif state ==2:
            self.label.setPixmap(QPixmap(os.path.join(self.equip_path,"filter2.png")))
            self.checkBoxf.setChecked(False)
    @pyqtSlot()
    def settingValueController(self):
        value =self.store.finaltag[self.variableid]
        self.toggle_images(value)
        
    def changingvalue(self):
        state = self.checkBoxf.checkState()
        if state == Qt.CheckState.Checked:
            self.store.settingValueOPC(self.variableid,1)
        elif state == Qt.CheckState.Unchecked:
            self.store.settingValueOPC(self.variableid,2)
if __name__ == '__main__':
        app = QApplication(sys.argv)
        
        window = Filter()
        # window.setStyleSheet("background-color: lightblue;")
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        window.show()
        sys.exit(app.exec())

        

       