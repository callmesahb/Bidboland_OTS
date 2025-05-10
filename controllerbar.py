import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt6.QtGui import QPainter, QPolygon, QColor, QPalette
from PyQt6.QtCore import QTimer, QPoint, Qt
import random

class TriangleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.minval = 0
        self.maxval = 100
        self.rightValue = 50
        self.centerValue = 50

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
        self.draw_triangleR(qp)
        qp.end()

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

    def value_to_percent(self, value):
        if self.maxval == self.minval:
            return 0
        percent = ((value - self.minval) / (self.maxval - self.minval)) * 100
        return max(0, min(100, percent))  # کلپ بین 0 و 100

    def setRightValue(self, value):
        self.rightValue = value
        self.update()

    def setCentervalue(self, value):
        self.centerValue = value
        percent = self.value_to_percent(value)
        self.progress.setValue(int(percent))
        self.update()

    def setminmaxvalue(self, min_val, max_val):
        self.minval = min_val
        self.maxval = max_val
        firstdiv = round(min_val, self.count_decimal_places(max_val))
        seconddiv = round(min_val + (max_val - min_val) / 4, self.count_decimal_places(max_val))
        thirddiv = round(min_val + (max_val - min_val) / 2, self.count_decimal_places(max_val))
        forthdiv = round(min_val + (max_val - min_val) * 3 / 4, self.count_decimal_places(max_val))
        fifthdiv = round(max_val, self.count_decimal_places(max_val))

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
        self.draw_colorbar(qp)
        # self.draw_guideline(qp)
        self.draw_triangleR(qp)
        qp.end()

    def getRanges(self,min:float,LL:float,L:float,H:float,HH:float) -> list:
        outlist = [min,LL,L,H,HH]
        return outlist


    def draw_colorbar(self, qp):
        # مشخصات مستطیل رنگی
        x = self.progress.geometry().right() + 3         # مکان افقی نوار رنگی
        y = 15        # مکان عمودی شروع نوار
        width = 5     # عرض نوار
        height = 200  # ارتفاع کل نوار

        section_height = height // 5

        colors = [
            QColor(255, 0, 0),     # قرمز پایین
            QColor(255, 255, 0),   # زرد
            QColor(0, 255, 0),     # سبز وسط
            QColor(255, 255, 0),   # زرد
            QColor(255, 0, 0)      # قرمز بالا
        ]

        for i, color in enumerate(colors):
            qp.setBrush(color)
            qp.setPen(Qt.PenStyle.NoPen)
            qp.drawRect(x, y + i * section_height, width, section_height)
