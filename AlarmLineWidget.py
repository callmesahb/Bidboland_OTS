from PyQt6 import QtWidgets,QtCore,QtGui
import os
from Store import Store
import sys

class AlarmLineWidget(QtWidgets.QWidget):
    linecolored = QtCore.pyqtSignal(str)
    def __init__(self,points,store:Store,line,connection,action):
        super().__init__()
        self.points = points
        self.store = store
        self.lineid = line
        self.connection = connection
        self.action = action
        # self.setFixedSize(1000,800)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.path = self.create_path_from_points(points)
        self.color = QtCore.Qt.GlobalColor.blue
        if len(points) >= 2:
            self.arrow_triangle = self.compute_arrow(points[-2], points[-1])
        else:
            self.arrow_triangle = None
            
        w,h = self.get_bounds()
        self.setFixedSize(int(w),int(h))
      
    def get_bounds(self):
        max_x = max(point[0] for point in self.points) + 20
        max_y = max(point[1] for point in self.points) + 20
        return max_x, max_y
      
    def compute_arrow(self, from_point, to_point):
        fx, fy, _ = from_point
        tx, ty, _ = to_point
        dx, dy = tx - fx, ty - fy
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length == 0:
            return None

        norm_dx, norm_dy = dx / length, dy / length
        perp_dx, perp_dy = -norm_dy, norm_dx

        arrow_size = 10
        p1 = QtCore.QPointF(tx, ty)
        p2 = QtCore.QPointF(tx - norm_dx * arrow_size + perp_dx * arrow_size / 2,
                            ty - norm_dy * arrow_size + perp_dy * arrow_size / 2)
        p3 = QtCore.QPointF(tx - norm_dx * arrow_size - perp_dx * arrow_size / 2,
                            ty - norm_dy * arrow_size - perp_dy * arrow_size / 2)

        return QtGui.QPolygonF([p1, p2, p3])
    def create_path_from_points(self, points):
        path = QtGui.QPainterPath()
        for x, y, cmd in points:
            if cmd == "M":
                path.moveTo(x, y)
            elif cmd == "L":
                path.lineTo(x, y)
        return path

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Draw line
        pen = QtGui.QPen(self.color, 2)
        painter.setPen(pen)
        painter.drawPath(self.path)

        # Draw arrow
        if self.arrow_triangle:
            brush = QtGui.QBrush(self.color)
            painter.setBrush(brush)
            painter.drawPolygon(self.arrow_triangle)
        
        
    # def paintEvent(self, event):
    #     painter = QtGui.QPainter(self)
    #     painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    #     # استفاده از QColor با alpha
    #     pen = QtGui.QPen()
    #     pen.setColor(self.color)
    #     pen.setWidth(3)

    #     painter.setPen(pen)

    #     path = QtGui.QPainterPath()
    #     if self.points:
    #         path.moveTo(*self.points[0])
    #         for pt in self.points[1:]:
    #             path.lineTo(*pt)

    #     painter.drawPath(path)

        
    # def set_color(self, trigger_id):
    #     state = self.store.finaltag.get(trigger_id, 0)
    #     if state == 1:
    #         self.color = QtGui.QColor("blue")
    #     elif state == 2:
    #         self.color = QtGui.QColor("red")
    #     else:
    #         self.color = QtGui.QColor("gray")
    #     self.update()  # این باعث اجرای دوباره paintEvent میشه
        
        
    # def set_color(self, trigger_id):
    #     state = self.store.finaltag.get(trigger_id, 0)

    #     if state == 1:
    #         # آبی با شفافیت (0 = کاملاً شفاف، 255 = کاملاً مات)
    #         self.color = QtGui.QColor(0, 0, 255, 80)  # آبی نیمه شفاف
    #     elif state == 2:
    #         self.color = QtGui.QColor(255, 0, 0, 255)  # قرمز کاملاً مات
    #     else:
    #         self.color = QtGui.QColor(0, 0, 255, 0)  # خاکستری با شفافیت نسبی

    #     self.update()




    def set_color(self,state):
        
        # 🎨 رنگ خود خط
        if state == 1:
            self.color = QtGui.QColor(0, 0, 255, 0)
            
        elif state == 2:
            self.color = QtGui.QColor(255, 0, 0, 255)
        else:
            self.color = QtGui.QColor(0, 0, 255, 0)

        self.repaint()
        
        
    def setting_color(self,state):
        
        # 🎨 رنگ خود خط
        if state == 1:
            self.color = QtGui.QColor(0, 0, 255, 0)
            
        elif state == 2:
            self.color = QtGui.QColor(255, 0, 0, 255)
        else:
            self.color = QtGui.QColor(0, 0, 255, 0)

        self.repaint()

        # 🎨 حالا رنگ خطوط متصل رو هم تغییر بده

    @QtCore.pyqtSlot()
    def updateLine(self):
        value = self.store.finaltag[self.lineid]
        if value == 1:
            self.store.settingValueOPC(self.connection,1)
            xvalue = self.store.finaltag[self.connection]
            self.setting_color(value)
            contid = self.connection[:-1]
            self.store.settingValueOPC(contid,1)
            self.set_color(value)
            # self.store.settingValueOPC(self.action[0],1)
        elif value == 2:
            self.store.settingValueOPC(self.connection,2)
            contid = self.connection[:-1]
            xvalue = self.store.finaltag[self.connection]
            self.setting_color(value)
            if self.action[1][0] == "u":
                self.store.settingValueOPC(self.action[0],1)
            else:
                self.store.settingValueOPC(self.action[0],2)
            # opvalue = self.store.finaltag["420P103A"]
            self.store.settingValueOPC(contid,2)
        # for id in self.connected:
        #     value1 = self.store.finaltag[id]
        #     self.set_color(value1,self.connected)
            self.set_color(value)
            
        # valuepb01 = self.store.finaltag["1PB001"]
        # valuepb02 = self.store.finaltag["1PB002"]
        # valueofesd3905 = self.store.finaltag["1ESD3905L"]
        # self.store.settingValueOPC("1PB001L",valueofesd3905)
        
        # self.set_color(connectionvalue)
        self.update()
        
    
    @QtCore.pyqtSlot(str)
    def updatebuttoncolor(self,name:str):
        # if name == "ON":
        #     self.store.settingValueOPC("1PB002L",2)
        #     self.store.settingValueOPC("1PB001L",2)
        #     self.set_color(2)
        # elif name == "OFF":
        #     self.store.settingValueOPC("1PB002L",1)
        #     self.store.settingValueOPC("1PB001L",1)
        #     self.set_color(1)
        
        pass

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    points = [
        [1089, 192, "M"],
              [1089, 439, "L"],
              [1089, 235, "L"],
              [1406, 235, "L"]
    ]

    win = AlarmLineWidget(points)
    win.show()
    sys.exit(app.exec())