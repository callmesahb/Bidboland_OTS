from PyQt6 import QtWidgets, QtGui,QtCore
from PyQt6.QtCore import Qt, pyqtSlot
from centralwidget import MainWidget
from AppToolbar import Toolbar
from Menubar import Menu
# from toolbar import AppToolbar
from Store import Store
import datetime
import os

class MainWindow(QtWidgets.QMainWindow):
    updatevalues = QtCore.pyqtSignal()
    def __init__(self,data,store:Store):
        super().__init__()

        self.rootdir = os.getcwd()
        self.data = data
        self.store = store
        self.menu = Menu(self.data)
        self.menu.left.clicked.connect(self.Printing)
        self.Currentindex = 0
        self.page = self.data["layout"]["sections"]
        self.store.updatevalues.connect(self.update)
        self._initUI()
        self.getPageOrder()
        self.drawFirstPage()
        self.drawoverviews()
        self.DeactiveChildFoucus()
        
    def _initUI(self):
        self.setWindowTitle("OTS 5")
        self.cntwidget = MainWidget(self.store)
        self.cntwidget.changePageSignal.connect(self.gotoPage)
        self.setCentralWidget(self.cntwidget)
        self.toolbar = Toolbar(self.store)
        self.addToolBar(self.toolbar)
        
    def drawFirstPage(self):
        self.centralWidget().createAllscenes(self.page)
        self.centralWidget().SetActiveScene(self.Currentindex)
        desc = self.store.ListingDescs(0)["description"]
        page = self.store.ListingDescs(0)["page"]
        self.cntwidget.updateDesc(desc)
        self.cntwidget.updatepage(page)
        self.cntwidget.update()
        

    @pyqtSlot(int)    
    def getPageOrder(self):
        self.pageorder = {}
        # print("salam")
        i = 0
        for data in self.page:
            self.pageorder[data["id"]] = i
            # print(i)
            i = i + 1
    # def CheckingParentId(self):

    def drawoverviews(self):
        if self.page[self.Currentindex]["overview"]:
            self.centralWidget().SetActiveScene(self.Currentindex)
    def nextpagenotoverview(self):
        if self.page[self.Currentindex]["overview"] == False:
            self.centralWidget().SetActiveScene(self.Currentindex)

            
    def nextPage(self):
        if self.Currentindex + 1 < len(self.page):
            if self.page[self.Currentindex]["parentId"] == 0:
                self.Currentindex = self.Currentindex + 1
                # if self.Currentindex == 6:
                #     self.Currentindex = self.Currentindex - 1
                desc = self.store.ListingDescs(self.Currentindex)["description"]
                page = self.store.ListingDescs(self.Currentindex)["page"]
                self.cntwidget.updateDesc(desc)
                self.cntwidget.updatepage(page)
                self.drawoverviews()
            if self.page[self.Currentindex]["parentId"] != 0:
                old_id = self.page[self.Currentindex]["parentId"]
                self.Currentindex = self.Currentindex + 1
                new_id = self.page[self.Currentindex]["parentId"]
                if old_id == new_id:
                    desc = self.store.ListingDescs(self.Currentindex)["description"]
                    page = self.store.ListingDescs(self.Currentindex)["page"]
                    self.cntwidget.updateDesc(desc)
                    self.cntwidget.updatepage(page)
                    self.nextpagenotoverview()
            self.centralWidget().update()

    def exPage(self):
        if self.Currentindex >= 1:
            if self.page[self.Currentindex]["parentId"] == 0:
                self.Currentindex = self.Currentindex - 1
                desc = self.store.ListingDescs(self.Currentindex)["description"]
                page = self.store.ListingDescs(self.Currentindex)["page"]
                self.cntwidget.updateDesc(desc)
                self.cntwidget.updatepage(page)
                self.drawoverviews()
            if self.page[self.Currentindex]["parentId"] != 0:
                old_id = self.page[self.Currentindex]["parentId"]
                # print(self.Currentindex)
                self.Currentindex = self.Currentindex - 1
                # print(self.Currentindex)
                new_id = self.page[self.Currentindex]["parentId"]
                if old_id == new_id:
                    desc = self.store.ListingDescs(self.Currentindex)["description"]
                    page = self.store.ListingDescs(self.Currentindex)["page"]
                    self.cntwidget.updateDesc(desc)
                    self.cntwidget.updatepage(page)
                    self.nextpagenotoverview()
            self.centralWidget().update()
            # else:
            #     self.drawOtherPages()
                
    def drawOtherPages(self):
        for page in self.page:
            if page["parentId"] != 0:
                self.centralWidget().SetActiveScene(self.Currentindex)
    
    @pyqtSlot(int)
    def gotoPage(self,pageId:int):
        if pageId in self.pageorder:
            self.Currentindex = self.pageorder[pageId]
            desc = self.store.ListingDescs(self.Currentindex)["description"]
            self.cntwidget.updateDesc(desc)
            self.centralWidget().SetActiveScene(self.Currentindex)
            
    def DeactiveChildFoucus(self):
        for child in self.findChildren(QtWidgets.QWidget):
            child.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    @pyqtSlot()
    def Printing(self):
        print("SALAMMM")
        
    def ChangingByClick(self):
        
        print("Changing is Correct")
        self.btn = self.menu.PRC
        self.btn.clicked.connect(self.Printing)

            
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key.Key_Right:
            self.nextPage()
        elif event.key() == Qt.Key.Key_Left:
            self.exPage()
        elif event.key() == Qt.Key.Key_Up:
            print(self.Currentindex)
            id = self.store.ListingDescs(self.Currentindex)["parentId"]
            if id == 20:
                self.Currentindex = 0
                self.centralWidget().SetActiveScene(self.Currentindex)
            if id == 30:
                self.Currentindex = 1
                self.centralWidget().SetActiveScene(self.Currentindex)
            if id == 31:
                self.Currentindex = 2
                self.centralWidget().SetActiveScene(self.Currentindex)
            if id == 40:
                self.Currentindex = 3
                self.centralWidget().SetActiveScene(self.Currentindex)
            if id == 2:
                self.Currentindex = 4
                self.centralWidget().SetActiveScene(self.Currentindex)
            if id == 1:
                self.Currentindex = 5
                self.centralWidget().SetActiveScene(self.Currentindex)
            
    @pyqtSlot()
    def update(self):
        timerstc = datetime.timedelta(seconds=self.store.finaltag["407EDTIMER"])
        self.toolbar.timer.setText("Timer:"+str(timerstc))
        # self.cntwidget.update_widgets(data)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()