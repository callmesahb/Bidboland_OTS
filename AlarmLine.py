from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QMainWindow,QWidget
from PyQt6.QtGui import QPainterPath, QPen, QColor, QBrush, QPolygonF
from PyQt6.QtCore import Qt, QTimer, QPointF
import sys



class AlarmLine(QGraphicsPathItem):
    def __init__(self, points):
        super().__init__()
        self.path = QPainterPath()
        self.points = points
        self.line_data= {
        "Line0": [[1.5, 245, "M"], [271.5, 245, "L"]],
        "Line1": [[283.5, 179, "M"], [283.5, 381, "L"], [283.5, 289, "L"], [416.5, 289, "L"]],
        "Line2": [[144.5, 330, "M"], [278.5, 330, "L"]]
        }
        self.logic_data= {"Line1": {"condition": ["Line0", "Line2", "0TAHH009"],"action": ["403ARS0EV013", "close"]}}
        self.alarm_data= {"0TAHH009": 1}
        self.blinking_lines={}
        self.setPath(self.make_path(points))
        self.setPen(QPen(Qt.GlobalColor.green, 3))
        self.blinking = False
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_color)
        self.visible = True

        last_two = points[-2:]
        if len(last_two) >= 2:
            self.arrow_item = QGraphicsPathItem()
            self.arrow_item.setPen(QPen(Qt.PenStyle.NoPen))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.green))
            self.arrow_item.setZValue(1)
            self.set_arrow(points[-2], points[-1])

    def make_path(self, points):
        path = QPainterPath()
        for pt in points:
            x, y, cmd = pt
            if cmd == "M":
                path.moveTo(x, y)
            elif cmd == "L":
                path.lineTo(x, y)
        return path

    def set_arrow(self, from_point, to_point):
        fx, fy, _ = from_point
        tx, ty, _ = to_point
        dx, dy = tx - fx, ty - fy
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length == 0:
            return
        norm_dx, norm_dy = dx / length, dy / length
        perp_dx, perp_dy = -norm_dy, norm_dx

        arrow_size = 10
        p1 = QPointF(tx, ty)
        p2 = QPointF(tx - norm_dx * arrow_size + perp_dx * arrow_size / 2,
                     ty - norm_dy * arrow_size + perp_dy * arrow_size / 2)
        p3 = QPointF(tx - norm_dx * arrow_size - perp_dx * arrow_size / 2,
                     ty - norm_dy * arrow_size - perp_dy * arrow_size / 2)

        triangle = QPolygonF([p1, p2, p3])
        path = QPainterPath()
        path.addPolygon(triangle)
        self.arrow_item.setPath(path)

    def start_blinking(self):
        if not self.blinking:
            self.blinking = True
            self.blinking_lines[self.line_id] = True
            self.blink_timer.start(500)

    def stop_blinking(self):
        if self.blinking:
            self.blinking = False
            self.blinking_lines[self.line_id] = False
            self.setPen(QPen(Qt.GlobalColor.green, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.green))
            self.blink_timer.stop()

    def toggle_color(self):
        if self.visible:
            self.setPen(QPen(Qt.GlobalColor.red, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))
        else:
            self.setPen(QPen(Qt.GlobalColor.green, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.green))
        self.visible = not self.visible