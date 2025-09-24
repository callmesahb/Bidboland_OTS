
from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QMouseEvent,QTransform
from PyQt6.QtCore import Qt,pyqtSignal,pyqtSlot
from PumpFacePlate import PumpFacePlate
import sys
import os
import time
import random
from Store import Store
from PyQt6 import QtWidgets,QtCore,QtGui
from HandSwitch import HandSwitch
import sys

class Equipment(QtWidgets.QWidget):
    ChangeHand = pyqtSignal()
    updatevalues = pyqtSignal(int)
    def __init__(self,name,type,btns,store):
        super().__init__()
        self.type = type
        self.name = name
        self.btns = btns
        self.store = store



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
        self.set_status(1)


    def load_image(self):
            self.image = {
                "h1": QPixmap(os.path.join(self.equip_path,"h_1.png")),
                "h2": QPixmap(os.path.join(self.equip_path,"h_2.png")),
                "h3":QPixmap(os.path.join(self.equip_path,"h_3.png")),
                "h4":QPixmap(os.path.join(self.equip_path,"h_4.png"))
                

            }

    def set_status(self , status):
        
        if self.name == "4201HS002":

            if status == 1:
                self.image_label.setPixmap(self.image["h3"])
            elif status == 2:
                self.image_label.setPixmap(self.image["h4"])
        elif self.name == "4201HS028":

            if status == 1:
                self.image_label.setPixmap(self.image["h2"])
            if status == 2:
                self.image_label.setPixmap(self.image["h1"])
                
        self.update()


    @pyqtSlot()         
    def ReadingValue(self):

        value = self.store.finaltag[self.name]
        self.set_status(value)  
        self.update()
        
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.type == "handswitch":
                self.hs = HandSwitch(self.name,self.btns,self.store)
                self.hs.show()