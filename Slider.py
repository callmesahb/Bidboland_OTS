from PyQt6 import QtWidgets,QtCore
from Store import Store
import sys

class Slider(QtWidgets.QWidget):
    updatevalues = QtCore.pyqtSignal()
    def __init__(self,rotated,w,h,op,name,store:Store,variableid):
        super().__init__()
        self.rotated = rotated
        self.w = w
        self.h = h
        self.op = op
        self.name = name
        self.store = store
        self.variableid = variableid
        # self.store.updatevalues.connect(self.updateSlider)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # print(self.rotated)
        
        self.InitUI()
    def InitUI(self):
        self.hlayout = QtWidgets.QHBoxLayout()
        self.ProgressBar()
        # self.settingRotation()
        
    def ProgressBar(self):
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(int(self.op))
        self.progress_bar.setTextVisible(False)
        self.valuelabel = QtWidgets.QLabel(f"{self.op}")
        
        self.setLayout(self.hlayout)
        if self.rotated == "left":
            self.progress_bar.setOrientation(QtCore.Qt.Orientation.Horizontal)
            self.progress_bar.setFixedSize(self.w,self.h)
            self.hlayout.addWidget(self.progress_bar)
            self.hlayout.addWidget(self.valuelabel)
        if self.rotated == "":
            self.progress_bar.setOrientation(QtCore.Qt.Orientation.Vertical)
            self.progress_bar.setFixedSize(self.w,self.h)
            self.hlayout.addWidget(self.progress_bar)
            self.hlayout.addWidget(self.valuelabel)
        if self.rotated == "right":
            pass
        if self.name[0] == "S":
            self.valuelabel.setHidden(True)
        self.progress_bar.setFixedSize(self.w, self.h)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2e2e2e;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #00FF00;
                margin: 0px;
            }
        """)


            
    @QtCore.pyqtSlot()
    def updateSlider(self):
        value = self.store.finaltag[self.variableid]
        self.progress_bar.setValue(int(value))
        self.valuelabel.setText(str(value))
        self.update()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Slider()
    ex.show()
    # ex.timer.start(1000)
    sys.exit(app.exec())