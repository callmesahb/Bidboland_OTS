from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot,QTimer
from Store import Store
from Link import Link
from Indicator import Indicator
# from valveEV import valveEV
from dosing import DosingPump
from Store import Store
from AirCoolerElem import Aircooler
from Menubar import Menu
from BPS_elem import BPS
from FilterElem import Filter
from Equipment import Equipment
from Pump import NormalPump
from controllerValve import ControllerValve
from Trend import Trend
from Slider import Slider
from HAND import HAND
from AlarmLine import AlarmLine
from ESDwidget import ESD
from valvetest import valveEV
import os
import json

class MainWidget(QtWidgets.QWidget):
    changePageSignal = pyqtSignal(int)
    ChangingValveStatus = pyqtSignal(int)
    updatevalues = pyqtSignal(dict,list)

    def __init__(self, store: Store):
        super().__init__()
        self.rootdir = os.getcwd()
        self.imgdir = os.path.join(self.rootdir, "images")
        self.store = store
        self.cache = {}
        
        self._initUi()
        self._addMenu()
        self._addGraphic()

    def _initUi(self):
        self.mainlayout = QtWidgets.QHBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainlayout)

    def _addMenu(self):
        self.menu = Menu(self.store)
        self.mainlayout.addWidget(self.menu)
        # self.menu.left.clicked.connect(self.Printing)
    
    def updateDesc(self,desc:str):
        # print(f"Updating to {desc}")
        self.menu.desc.setText(desc)
    def updatepage(self,desc:str):
        self.menu.pagenum.setText(desc)
    def _addGraphic(self):
        self.graphicsview = QtWidgets.QGraphicsView()
        self.graphicsscene = QtWidgets.QGraphicsScene()
        self.graphicsview.setScene(self.graphicsscene)
        self.graphicsview.setStyleSheet("background-color: rgb(103, 103, 103);")
        self.mainlayout.addWidget(self.graphicsview)
        
    def normalize_pos(self,pos,img_width,img_height):
        # return (
        #     int(pos["l"] / 100 * img_width),
        #     int(pos["t"] / 100 * img_height),
        #     int(pos["w"] / 100 * img_width),
        #     int(pos["h"] / 100 * img_height),
        # )
        l = max(0, int(pos["l"] / 100 * img_width))
        t = max(0, int(pos["t"] / 100 * img_height))
        w = max(10, int(pos["w"] / 100 * img_width))
        h = max(10, int(pos["h"] / 100 * img_height))
        return l,t,w,h

    def newImage(self, img: QtGui.QPixmap) -> QtGui.QPixmap:
        img_width = img.size().width()
        img_height = img.size().height()
        screen_width = self.screen().size().width()
        screen_height = 0.88 * self.screen().size().height()
        width_scale = screen_width / img_width
        height_scale = screen_height / img_height

        self.scale = min(width_scale, height_scale)
        # print(self.scale)

        newimg_width = int(img_width * self.scale)
        newimg_height = int(img_height * self.scale)

        newImg = img.scaled(newimg_width, newimg_height)

        return img
    def createAllscenes(self, pages: list):
        self.scenes = []
        screen_width = self.screen().size().width()
        screen_height = 0.88 * self.screen().size().height()
        scales = []
        for page in pages:
            tempScene = QtWidgets.QGraphicsScene()
            img_path = os.path.join(self.rootdir, page["imageUrl"])
            mainImage = QtGui.QPixmap(img_path)
            print(page["imageUrl"])
            self.scaledImage = self.newImage(mainImage)
            img_width = mainImage.width()
            img_height = mainImage.height()
            width_scale = screen_width / img_width
            height_scale = screen_height / img_height
            scales.append(min(width_scale,height_scale))
            if scales:
                self.scale = sum(scales)/ len(scales)
            else:
                self.scale = 1.0
            tempScene.addPixmap(mainImage)
            for _ind in page["indicators"]:
                pos = _ind["pos"]
                print(pos["l"])
                # l,t,w,h = self.normalize_pos(int(pos["l"],pos["t"],pos["w"],pos["h"]))
                name = _ind["id"]
                variableid = _ind["variableId"]
                itype = _ind["type"]
                value = self.store.SettingInitial(variableid)
                pvvalues = self.store.GettingControllerDetails(variableid)
                # value = self.store.opc.getValue(variableid)
                # print(f"{name}:{variableid}:{value}")
                self.indi = Indicator(name, value, itype, pvvalues,self.store,variableid)
                self.indi.setGeometry(int(pos["l"]),int(pos["t"]),80,20)
                self.store.updatevalues.connect(self.indi.updatinvalue)
                self.indi.TrendRequested.connect(self.showingTrend)
                # self.indi.Value.setText(str(round(value,2)))
                tempScene.addWidget(self.indi)
            for _link in page["links"]:
                pos = _link["pos"]
                # l,t,w,h = self.normalize_pos(pos,img_width,img_height)
                dest = _link["to"]
                link = Link(dest)
                link.setGeometry(int(pos["l"]),int(pos["t"]),int(pos["w"]),int(pos["h"]))
                link.changePageSignal.connect(self.ChangePageByLink)
                tempScene.addWidget(link)
            for _valve in page["valves"]:
                pos = _valve["pos"]
                variableid = _valve["variableId"]
                name = _valve["id"]
                _type = _valve["type"]
                rotated = _valve["rotated"]
                valve = None

                value = self.store.setting_valueEV(variableid) if _type != "controller" else None

                if _type == "controller" and variableid in self.store.getting_names():
                    # print(self.store.getting_names())
                    pvvalues = self.store.GettingControllerDetails(variableid)
                    valve = ControllerValve(name, rotated, pvvalues,variableid,self.store)
                    self.store.updatevalues.connect(valve.settingValueController)
                elif _type in {"sdv", "bdv"}:
                    valve = valveEV(self.store,variableid,name, value,rotated)
                    self.store.updatevalues.connect(valve.ReadingValue)
                    # valve.ChangingValveStatus.connect(self.CheckingvalueSDV)
                    # valve.set_status(value)
                elif _type == "dosing":
                    valve =DosingPump(self.store,variableid, value,rotated)
                    self.store.updatevalues.connect(valve.ReadingValue)
                    # valve.set_status(value)
                elif _type == "fan":
                    valve = Aircooler(self.store,variableid,name, value)
                    self.store.updatevalues.connect(valve.ReadingValue)
                    # valve.set_status(value)
                elif _type == "bps":
                    valve = BPS(self.store,variableid,name, value)
                    valve.set_status(value)
                elif _type == "Filter":
                    valve =Filter(self.store,variableid,name, value)
                    # valve.toggle_images(value)
                    self.store.updatevalues.connect(valve.settingValueController)
                elif _type == "pump":
                    valve =NormalPump(self.store,variableid,name, value,rotated)
                    # valve.set_status(value)
                    self.store.updatevalues.connect(valve.ReadingValue)

                if valve:
                    valve.setGeometry(
                        int(pos["l"]),
                        int(pos["t"]),
                        int(pos["w"]),
                        int(pos["h"]),
                    )
                    tempScene.addWidget(valve)
            for _slider in page["sliders"]:
                pos = _slider["pos"]
                w = pos["w"]
                h = pos["h"]
                name = _slider["id"]
                variableid = _slider["variableId"]
                pvvalues = self.store.GettingControllerDetails(variableid)
                rotated = _slider["rotated"]
                slider = Slider(rotated, w, h, pvvalues[2],name,self.store,variableid)
                slider.setGeometry(int(pos["l"]), int(pos["t"]), int(pos["w"]),
                                   int(pos["h"]))
                self.store.updatevalues.connect(slider.updateSlider)
                tempScene.addWidget(slider)
            for _eqn in page["equipments"]:
                _id = _eqn["id"]
                pos = _eqn["pos"]
                htype = _eqn["type"]
                btns = _eqn["buttons"]
                eqn = Equipment(_id,htype,btns)
                eqn.setGeometry(int(pos["l"]), int(pos["t"]), int(pos["w"]),
                                   int(pos["h"]))
                tempScene.addWidget(eqn)
            for hand in page["indicators"]:
                pos = hand["pos"]
                variableid = hand["variableId"]
                dtype = hand["type"]
                if dtype == "controller":
                    dast = HAND(self.store,variableid)
                    dast.setGeometry(int(pos["l"])+80, int(pos["t"])-35, 15, 20)
                    tempScene.addWidget(dast)
                    # dast.set_status(1)
                    self.store.updatevalues.connect(dast.ReadingValue)
            for _line in page["lines"]:
                pos = _line["points"]
                line = AlarmLine(pos)
                tempScene.addItem(line)
                if hasattr(line, "arrow_item"):
                    tempScene.addItem(line.arrow_item)
                    
            for _esd in page["esds"]:
                pos = _esd["pos"]
                id = _esd["id"]
                esd = ESD(id)
                esd.setGeometry(int(self.scale*pos["l"]), int(self.scale*pos["t"]), int(self.scale*pos["w"]),
                                   int(self.scale*pos["h"]))
                tempScene.addWidget(esd)
            self.scenes.append(tempScene)
    def SetActiveScene(self, SceneIndex: int):
        self.graphicsview.setScene(self.scenes[SceneIndex])
        # self.graphicsview.setTransform(QtGui.QTransform().scale(self.scale,self.scale))
        # self.graphicsview.fitInView(self.scenes[SceneIndex].sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
    def resizeEvent(self, a0):
        self.graphicsview.setTransform(QtGui.QTransform().scale(self.scale, self.scale))
        super().resizeEvent(a0)
        
        


    @pyqtSlot(int)
    def ChangePageByLink(self, dest):
        self.changePageSignal.emit(dest)
    
    @pyqtSlot(str)
    def showingTrend(self):
        trend = Trend(self)
    
    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        # self.graphicsview.fitInView(self.scenes[SceneIndex].sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.graphicsview.fitInView(QtCore.QRectF(self.scaledImage.rect()), QtCore.Qt.AspectRatioMode.IgnoreAspectRatio)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWidget()
    window.showMaximized()
    pages = json.loads(
        open(r"D:\\Petro\\New_OTS\\data\\data.json", "r").read())
    page = pages["layout"]["sections"]
    window.createAllscenes(page)
    window.SetActiveScene(0)
    app.exec()