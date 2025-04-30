from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QMainWindow,QWidget
from PyQt6.QtGui import QPainterPath, QPen, QColor, QBrush, QPolygonF
from PyQt6.QtCore import Qt, QTimer, QPointF,pyqtSignal,QObject
from Store import Store
from ESDAction import Action
import sys



class SignalEmitter(QObject):
    done_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

class AlarmLine(QGraphicsPathItem):
    def __init__(self, points,connected,action:list,store:Store,lineid:str):
        super().__init__()
        self.path = QPainterPath()
        self.points = points
        self.connected = connected
        self.action = action
        self.store = store
        self.lineid = lineid
        self.signals = SignalEmitter()
        # print(connected)
        self.color = "default"
        self.connected_lines = []
        self.line_data= {}
        self.logic_data= {}
        self.alarm_data= {}
        self.blinking_lines={}
        self.setPath(self.make_path(points))
        self.setPen(QPen(Qt.GlobalColor.blue, 3))
        self.blinking = False
        self.status = "NORMAL"
        self.doinAction = Action(self.action,self.store)
        self.actiontimer = QTimer()
        self.actiontimer.timeout.connect(self.alarm_triggered)
        self.visible = True

        last_two = points[-2:]
        if len(last_two) >= 2:
            self.arrow_item = QGraphicsPathItem()
            self.arrow_item.setPen(QPen(Qt.PenStyle.NoPen))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
            self.arrow_item.setZValue(1)
            self.set_arrow(points[-2], points[-1])
            
        self.lineid = None
        
    def set_connected_lines(self,line_objects):
        self.connected_lines = line_objects
    def set_color(self, color):
        self.color = color

        if color == "red":
            self.setPen(QPen(Qt.GlobalColor.red, 3))
            if hasattr(self, "arrow_item"):
                self.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))
                self.status = "ALARM"
        else:
            self.setPen(QPen(Qt.GlobalColor.blue, 3))
            if hasattr(self, "arrow_item"):
                self.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
                self.status = "NORMAL"

        if self.scene():
            self.scene().update()


        for connected_line in self.connected_lines:
            if color == "red":
                QTimer.singleShot(2000, lambda line=connected_line: self.set_connected_line_red(line))
            else:
                connected_line.set_color("green")
                if connected_line.scene():
                    connected_line.scene().update()

    def set_connected_line_red(self, line):
        line.set_color("red")
        if line.scene():
            line.scene().update()



    
    def update_color(self):
        self.set_color("red")
        if self.color == "red":
            for connected_line in self.connected_lines:
                QTimer.singleShot(2000,lambda:connected_line.set_color("red"))
    def make_path(self, points):
        path = QPainterPath()
        for pt in points:
            x, y, cmd = pt
            if cmd == "M":
                path.moveTo(x, y)
            elif cmd == "L":
                path.lineTo(x, y)
        return path
    
    
    def settting_color(self, status: str):
        if status == "ALARM":
            self.setPen(QPen(Qt.GlobalColor.red, 3))
            if hasattr(self, "arrow_item"):
                self.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))
        

            if self.connected and self.scene():
                for item in self.scene().items():
                    if isinstance(item, AlarmLine) and hasattr(item, 'lineid') and item.lineid == self.connected:
                        QTimer.singleShot(2000, lambda line=item: self._set_line_red(line))
                        self.status = "NORMAL"
                self.actiontimer.start(1000)

        else:
            self.setPen(QPen(Qt.GlobalColor.blue, 3))
            if hasattr(self, "arrow_item"):
                self.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
            
            self.actiontimer.stop()

            if self.connected and self.scene():
                for item in self.scene().items():
                    if isinstance(item, AlarmLine) and hasattr(item, 'lineid') and item.lineid == self.connected:
                        item.setPen(QPen(Qt.GlobalColor.blue, 3))
                        if hasattr(item, "arrow_item"):
                            item.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
                        item.update()

    def _set_line_red(self, line):
        line.setPen(QPen(Qt.GlobalColor.red, 3))
        if hasattr(line, "arrow_item"):
            line.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))
        line.update()



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
            self.setPen(QPen(Qt.GlobalColor.blue, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
            self.blink_timer.stop()

    def toggle_color(self):
        if self.visible:
            self.setPen(QPen(Qt.GlobalColor.red, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.red))
        else:
            self.setPen(QPen(Qt.GlobalColor.blue, 3))
            self.arrow_item.setBrush(QBrush(Qt.GlobalColor.blue))
        self.visible = not self.visible
    
        
    def alarm_triggered(self):
        for item in self.scene().items():
            if isinstance(item, AlarmLine) and hasattr(item, 'lineid') and item.lineid == self.connected:
                tag = item.action[0]
                action = item.action[1]
                emitted = self.connected[:-1]
                if action in ["shutdown", "close"]:
                    self.signals.done_signal.emit(emitted)
                    self.store.opc.setValue(tag, 2)
                    
                    
    