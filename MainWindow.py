from PyQt6 import QtWidgets, QtGui,QtCore
from PyQt6.QtCore import Qt, pyqtSlot
from centralwidget import MainWidget
from AppToolbar import Toolbar
from Menubar import Menu
from APIs import Aspen
# from toolbar import AppToolbar
from Store import Store
from Trend import Trend
import datetime
import os

class MainWindow(QtWidgets.QMainWindow):
    updatevalues = QtCore.pyqtSignal()
    def __init__(self,data,store:Store,tags):
        super().__init__()
        
        self.rootdir = os.getcwd()
        icondir = os.path.join(self.rootdir,"icons")
        simdir = os.path.join(self.rootdir,"sim")
        picdir = os.path.join(icondir,"BB_icon")
        self.setWindowIcon(QtGui.QIcon(picdir))
        self.data = data
        self.store = store
        self.tags = tags
        self.Currentindex = 0
        self.page = self.data["layout"]["sections"]
        self.store.updatevalues.connect(self.update)
        self.apis = Aspen(simdir)
        self._initUI()
        self.getPageOrder()
        self.drawFirstPage()
        self.drawoverviews()
        self.DeactiveChildFoucus()
        # self.menu = Menu(self.data)
        # print("Menu created:", self.menu)
        # # self.menu.changepage.connect(self.changingpage)
        # print("Signal connected to changingpage")
        
    def _initUI(self):
        self.setWindowTitle("OTS 2")
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet("""
            QTabBar::close-button {
                image: url(icons/close.png);
                subcontrol-position: right;
                margin: 2px;
            }
            QTabBar::close-button:hover {
                image: url(icons/close.png);
            }
            QTabBar::close-button:pressed {
                image: url(icons/close.png);
            }
        """)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabs)
        self.cntwidget = MainWidget(self.store)
        self.cntwidget.changepagecnt.connect(self.changingpage)
        self.cntwidget.changePageSignal.connect(self.gotoPage)
        self.cntwidget.changepagebyesd.connect(self.gotoPage)
        self.cntwidget.addToTabRequested.connect(self.addNewTab)
        self.tabs.addTab(self.cntwidget,"MAIN")
        # self.setCentralWidget(self.cntwidget)
        self.toolbar = Toolbar(self.store,self.tags)
        self.addToolBar(self.toolbar)
        self.toolbar.reset_signal.connect(self.cntwidget.reset_widgets)
        self.toolbar.rewind_triggered.connect(self.cntwidget.rewinding)
        self.toolbar.closeallwidgets.connect(self.cntwidget.Closing)
       
    def closeTab(self,index):
        widget = self.tabs.widget(index)
        if index == 0:
            return
        if widget is not None:
            widget.deleteLater()
        self.tabs.removeTab(index)
    @pyqtSlot(str)
    def changingpage(self,status:str):
        if status == "Back":
            self.exPage()
        if status == "Next":
            self.nextPage()
        if status == "Up":
            self.handle_up_logic()
        if status == "OV":
            self.drawFirstPage()
        if status == "First":
            self.handle_up_logic()
        if status == "ESD":
            self.handl_esd_page()
    def addNewTab(self, pageId):
        if pageId in self.pageorder:
            scene_index = self.pageorder[pageId]
            scene = self.cntwidget.scenes[scene_index]
            desc = self.store.ListingDescs(scene_index)["description"]
            page = self.store.ListingDescs(scene_index)["page"]
            # wrapper widget
            wrapper = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(wrapper)
            layout.setContentsMargins(0, 0, 0, 0)

            # Menu جدا بسازیم (مثل MainWidget)
            menu = Menu(self.store)
            menu.desc.setText(str(desc))
            menu.pagenum.setText(str(page))

            # QGraphicsView با scene اشتراکی
            view = QtWidgets.QGraphicsView()
            view.setStyleSheet("background-color:#676767")
            view.setScene(scene)

            layout.addWidget(menu)
            layout.addWidget(view)

            self.tabs.addTab(wrapper, f"Page {pageId}")
            self.tabs.setCurrentWidget(wrapper)
        if pageId not in self.pageorder:
            pass
    def drawFirstPage(self):
        self.cntwidget.createAllscenes(self.page)
        self.cntwidget.SetActiveScene(self.Currentindex)
        desc = self.store.ListingDescs(0)["description"]
        page = self.store.ListingDescs(0)["page"]
        self.cntwidget.updateDesc(desc)
        self.cntwidget.updatepage(page)
        self.cntwidget.update()
        


    # def Closing(self,state:bool):
    #     if state:
    #         self.cntwidget.Closing(state)
    #     else:
    #         print("SALAMMMMMMMM")


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
            self.cntwidget.SetActiveScene(self.Currentindex)
    def nextpagenotoverview(self):
        if self.page[self.Currentindex]["overview"] == False:
            self.cntwidget.SetActiveScene(self.Currentindex)

    def nextPage(self):
        if self.Currentindex + 1 < len(self.page):
            if self.page[self.Currentindex]["parentId"] == 0:
                self.Currentindex = self.Currentindex + 1
                if self.Currentindex == 3:
                    self.Currentindex = self.Currentindex - 1
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
                elif old_id != new_id:
                    self.Currentindex = self.Currentindex - 1
            self.cntwidget.update()

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
                elif old_id != new_id:
                    self.Currentindex = self.Currentindex + 1
            self.cntwidget.update()
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
            page = self.store.ListingDescs(self.Currentindex)["page"]
            self.cntwidget.updateDesc(desc)
            self.cntwidget.updatepage(page)
            self.update()
            self.cntwidget.SetActiveScene(self.Currentindex)
            
    def DeactiveChildFoucus(self):
        for child in self.findChildren(QtWidgets.QWidget):
            child.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
    @pyqtSlot(bool)
    def closeAllWidgets(self):
        print("Closing all widgets inside MainWidget")
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget is not self:
                widget.close()










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
            self.handle_up_logic()
            # if id == 40:
            #     self.Currentindex = 3
            #     self.centralWidget().SetActiveScene(self.Currentindex)
            # if id == 2:
            #     self.Currentindex = 4
            #     self.centralWidget().SetActiveScene(self.Currentindex)
            # if id == 1:
            #     self.Currentindex = 5
            #     self.centralWidget().SetActiveScene(self.Currentindex)
            # if id == 90:
            #     self.Currentindex = 6
            #     self.centralWidget().SetActiveScene(self.Currentindex)
    def handle_up_logic(self):
        print(self.Currentindex)
        id = self.store.ListingDescs(self.Currentindex)["parentId"]
        if id == 1:
            self.Currentindex = 0
        elif id == 3:
            self.Currentindex = 2
        elif id == 2:
            self.Currentindex = 1
        # elif id == 90:
        #     self.Currentindex = 3
        elif id == 0:
            self.Currentindex = 0
        else:
            return

        self.cntwidget.SetActiveScene(self.Currentindex)
        desc = self.store.ListingDescs(self.Currentindex)["description"]
        page = self.store.ListingDescs(self.Currentindex)["page"]
        self.cntwidget.updateDesc(desc)
        self.cntwidget.updatepage(page)
        
    def handl_esd_page(self):
        self.Currentindex = 3
        id = self.store.ListingDescs(self.Currentindex)["parentId"]

        self.cntwidget.SetActiveScene(self.Currentindex)
        desc = self.store.ListingDescs(self.Currentindex)["description"]
        page = self.store.ListingDescs(self.Currentindex)["page"]
        self.cntwidget.updateDesc(desc)
        self.cntwidget.updatepage(page)

    def closeEvent(self, a0: QtGui.QCloseEvent | None) -> None:
        self.apis.QuitSim()
        for window in QtWidgets.QApplication.topLevelWidgets():
            window.close()
        return super().closeEvent(a0)
            
    @pyqtSlot()
    def update(self):
        timer_value = int(self.store.finaltag["420TIMER"])
        hours, remainder = divmod(timer_value, 3600)
        minutes, seconds = divmod(remainder, 60)
        timestr = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.toolbar.timer.setText("Timer:"+str(timestr))
        # self.cntwidget.update_widgets(data)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()