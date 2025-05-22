import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt6.QtGui import QPainter, QPolygon, QColor, QPalette
from PyQt6.QtCore import QTimer, QPoint, Qt
import random

class TriangleWidget(QWidget):
    def __init__(self, LL:None,L:None,H:None,HH:None,parent=None):
        super().__init__()
        self.minval = 0
        self.maxval = 100
        self.rightValue = 50
        self.centerValue = 50
        self.low = L
        self.lowlow = LL
        self.high = H
        self.highhigh = HH
        self.setThresholds(self.lowlow,self.low,self.high,self.highhigh)
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Orientation.Vertical)
        self.progress.show()
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 255, 0))
        self.progress.setPalette(palette)
        self.progress.setGeometry(20, 15, 20, 200)
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

        self.initUI()

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
        self.label5.setGeometry(60, 196, 50, 20)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # self.draw_triangleR(qp)
        qp.end()
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
        return top + height - int(scale * height)


    # def setRightValue(self, value):
    #     self.rightValue = value
    #     self.update()

    def setCentervalue(self, value):
        self.centerValue = value
        # percent = self.value_to_percent(value)
        self.progress.setValue(int(value))
        self.update()

    def setminmaxvalue(self, min_val, max_val):
        self.minval = min_val
        self.maxval = max_val
        firstdiv = round(min_val, 3)
        seconddiv = round(min_val + (max_val - min_val) / 4,3)
        thirddiv = round(min_val + (max_val - min_val) / 2,3)
        forthdiv = round(min_val + (max_val - min_val) * 3 / 4,3)
        fifthdiv = round(max_val,3)

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
        """
        Draw yellow rectangles between LL-L and H-HH to indicate warning ranges.
        """
        x = self.progress.geometry().right() + 3  # مکان افقی نوار رنگی
        y_top = 15                                # مکان شروع Y
        width = 8
        height = 200

        def value_to_y(val):
            percent = self.value_to_percent(val)
            return y_top + height - int(percent / 100 * height)

        qp.setBrush(QColor(255, 255, 0))  # زرد
        qp.setPen(Qt.PenStyle.NoPen)

        # LL to L
        if 'LL' in kwargs and 'L' in kwargs:
            y1 = value_to_y(kwargs['LL'])
            y2 = value_to_y(kwargs['L'])
            qp.drawRect(x, min(y1, y2), width, abs(y2 - y1))

        # H to HH
        if 'H' in kwargs and 'HH' in kwargs:
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
