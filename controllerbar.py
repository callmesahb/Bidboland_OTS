import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt6.QtGui import QPainter, QPolygon, QColor, QPalette
from PyQt6.QtCore import QTimer, QPoint, Qt,pyqtSignal
import random
from Store import Store

class TriangleWidget(QWidget):
    gettingrangevalues = pyqtSignal(float,float)
    def __init__(self, LL:None,L:None,H:None,HH:None,variableid,store:Store,ranges,parent=None):
        super().__init__()
        self.minval = 0
        self.maxval = 100
        self.rightValue = 50
        self.centerValue = 50
        self.low = L
        self.lowlow = LL
        self.high = H
        self.highhigh = HH
        self.ranges = ranges
        self.store = store
        self.variableid = variableid
        self.setThresholds(self.lowlow,self.low,self.high,self.highhigh)
        
        # self.timer_range = QTimer()
        # self.timer_range.timeout.connect(self.settingrangesensor)
        # self.timer_range.start(1000)
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Orientation.Vertical)
        self.rightProgress = QProgressBar(self)
        self.leftvalue = 0.0
        self.rightProgress.setOrientation(Qt.Orientation.Vertical)
        self.rightProgress.setTextVisible(False)
        self.rightProgress.setGeometry(80, 15, 20, 300)
        self.progress.show()
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 255, 0))
        self.progress.setPalette(palette)
        self.progress.setGeometry(40, 15, 20, 200)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: rgb(0,255,1);
            }
        """)
        self.rightProgress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: rgb(0,255,1);
            }
        """)
        self.gettingrangevalues.connect(self.settingranges)
        self.initUI()


    def settingrangesensor(self):
        pvh = self.variableid + "PVH"
        pvl = self.variableid + "PVL"
        pvll = self.variableid + "PVLL"
        pvhh = self.variableid + "PVHH"
        pvhv = self.store.finaltag[pvh]
        pvlv = self.store.finaltag[pvl]
        pvhhv = self.store.finaltag[pvhh]
        pvllv = self.store.finaltag[pvll]
        self.setThresholds(pvllv,pvlv,pvhv,pvhhv)
    def gettinglvalues(self,h,l):
        self.gettingrangevalues.emit(h,l)
    def settingranges(self,h,l):
        pass
    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 110, 220)
        self.setFixedSize(110, 220)
        self.setWindowTitle('Triangle Progress')

        self.label1 = QLabel("_1400000", parent=self)
        self.label1.setGeometry(60, 0, 50, 20)
        self.label2 = QLabel("_1400000", parent=self)
        self.label2.setGeometry(60, 49, 50, 20)
        self.label3 = QLabel("_1400000", parent=self)
        self.label3.setGeometry(60, 98, 50, 20)
        self.label4 = QLabel("_1400000", parent=self)
        self.label4.setGeometry(60, 147, 50, 20)
        self.label5 = QLabel("_1400000", parent=self)
        self.label5.setGeometry(60, self.progress.height(), 50, 20)
        self.show()

    def value_to_percent(self, value):
        if self.maxval == self.minval:
            return 0
        return (value - self.minval) / (self.maxval - self.minval) * 100

    def draw_triangleR(self, qp):
        percent = self.value_to_percent(self.rightValue)
        y = int(self.progress.geometry().y()) - 50 + int(self.progress.height()) - int(percent / 100 * self.progress.height())
        qp.setBrush(QColor(255, 0, 0))
        points = [
            QPoint(40, 50 + y),
            QPoint(53, 42 + y),
            QPoint(53, 57 + y)
        ]
        triangle = QPolygon(points)
        qp.drawPolygon(triangle)

    def value_to_y(self, value):
        # اگر minval و maxval برابر باشند، ارتفاع 0 میشه
        if self.maxval == self.minval:
            return self.progress.geometry().y() + self.progress.height()
        
        height = self.progress.height()
        top = self.progress.geometry().y()
        scale = (value - self.minval) / (self.maxval - self.minval)
        return top + height - int(scale * height) + 10


    # def setRightValue(self, value):
    #     self.rightValue = value
    #     self.update()

    def draw_triangleL(self, qp):
        if not hasattr(self, 'leftValue'):
            return

        percent = self.value_to_percent(self.leftValue)
        y = int(self.progress.geometry().y()) + self.progress.height() - int(percent / 100 * self.progress.height())

        qp.setBrush(QColor(0, 0, 255))  # آبی
        points = [
            QPoint(30, y),
            QPoint(17, y - 8),
            QPoint(17, y + 8)
        ]
        triangle = QPolygon(points)
        qp.drawPolygon(triangle)

    def setCentervalue(self, value):
        self.centerValue = value
        # percent = self.value_to_percent(value)
        self.progress.setValue(int(value))
        self.update()

    def setminmaxvalue(self, min_val, max_val):
        self.minval = min_val
        self.maxval = max_val
        firstdiv = int(round(min_val,1))
        seconddiv = round(min_val + (max_val - min_val) / 4,1)
        thirddiv = round(min_val + (max_val - min_val) / 2,1)
        forthdiv = round(min_val + (max_val - min_val) * 3 / 4,1)
        fifthdiv = round(max_val,1)

        self.label5.setText(str(firstdiv))
        self.label4.setText(str(seconddiv))
        self.label3.setText(str(thirddiv))
        self.label2.setText(str(forthdiv))
        self.label1.setText(str(fifthdiv))

    def count_decimal_places(self, number):
        number_str = str(number)
        if '.' in number_str:
            return len(number_str.split('.')[1])
        return 0
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if hasattr(self,"thresholds"):
            self.draw_colorbar(qp,**self.thresholds)
        self.draw_triangleL(qp)
        # self.draw_colorbar(qp)
        # self.draw_guideline(qp)
        # self.draw_triangleR(qp)
        qp.end()

    def getRanges(self,min:float,LL:float,L:float,H:float,HH:float) -> list:
        outlist = [min,LL,L,H,HH]
        return outlist


    # def draw_colorbar(self, qp):
    #     # مشخصات مستطیل رنگی
    #     x = self.progress.geometry().right() + 3         # مکان افقی نوار رنگی
    #     y = 15        # مکان عمودی شروع نوار
    #     width = 5     # عرض نوار
    #     height = 200  # ارتفاع کل نوار

    #     section_height = height // 5

    #     colors = [
    #         QColor(255, 0, 0),     # قرمز پایین
    #         QColor(255, 255, 0),   # زرد
    #         QColor(0, 255, 0),     # سبز وسط
    #         QColor(255, 255, 0),   # زرد
    #         QColor(255, 0, 0)      # قرمز بالا
    #     ]

    #     for i, color in enumerate(colors):
    #         qp.setBrush(color)
    #         qp.setPen(Qt.PenStyle.NoPen)
    #         qp.drawRect(x, y + i * section_height, width, section_height)


    def draw_colorbar(self, qp, **kwargs):
        x = self.progress.geometry().right() + 3  # مکان افقی نوار رنگی
        y_top = self.progress.geometry().y()      # مبدا Y
        height = self.progress.height()
        width = 8

        def value_to_y(val):
            percent = self.value_to_percent(val)
            return y_top + height - int(percent / 100 * height)

        qp.setPen(Qt.PenStyle.NoPen)
        qp.setBrush(QColor(255, 255, 0))  # زرد

        # ناحیه LL تا L
        if kwargs.get('LL') is not None and kwargs.get('L') is not None:
            if kwargs['LL'] == kwargs['L']:
                y1 = value_to_y(kwargs['LL'])
                y2 = value_to_y(self.ranges[0])  # استفاده از حداقل رنج
            else:
                y1 = value_to_y(kwargs['LL'])
                y2 = value_to_y(kwargs['L'])
            qp.drawRect(x, min(y1, y2), width, abs(y2 - y1))

        # ناحیه H تا HH
        if kwargs.get('H') is not None and kwargs.get('HH') is not None:
            if kwargs['H'] == kwargs['HH']:
                y1 = value_to_y(kwargs['H'])
                y2 = value_to_y(self.ranges[1])  # استفاده از حداکثر رنج
            else:
                y1 = value_to_y(kwargs['H'])
                y2 = value_to_y(kwargs['HH'])
            qp.drawRect(x, min(y1, y2), width, abs(y2 - y1))


    def setThresholds(self, LL=None, L=None, H=None, HH=None):
        self.thresholds = {
            'LL': LL,
            'L': L,
            'H': H,
            'HH': HH
        }
        self.update()
    def setLeftValue(self, value):
        self.leftValue = value
        self.update()