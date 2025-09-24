# from PyQt6 import QtWidgets, QtCore
# import pyqtgraph as pg

# from PyQt6 import QtWidgets, QtCore
# import pyqtgraph as pg

# class TagPlotWidget(QtWidgets.QWidget):
#     def __init__(self, store, all_tags):
#         super().__init__()
#         self.store = store
#         self.all_tags = all_tags
#         self.active_tags = {}  # tag: (curve, data_list)
#         self.max_points = 100

#         self.init_ui()
#         self.start_timer()

#     def init_ui(self):
#         layout = QtWidgets.QHBoxLayout(self)

#         # ---- چپ: نمودار ----
#         self.plot_widget = pg.PlotWidget(title="multi Trend")
#         self.plot_widget.showGrid(x=True, y=True)
#         layout.addWidget(self.plot_widget, stretch=3)

#         # ---- راست: تب جستجو ----
#         self.tabs = QtWidgets.QTabWidget()
#         self.search_tab = QtWidgets.QWidget()
#         search_layout = QtWidgets.QVBoxLayout()

#         self.search_box = QtWidgets.QLineEdit()
#         self.search_box.setPlaceholderText("Search..")
#         self.search_box.textChanged.connect(self.filter_tags)
#         search_layout.addWidget(self.search_box)

#         self.tag_list = QtWidgets.QListWidget()
#         self.tag_list.addItems(self.all_tags)
#         self.tag_list.itemClicked.connect(self.add_tag_plot)
#         search_layout.addWidget(self.tag_list)

#         self.search_tab.setLayout(search_layout)
#         self.tabs.addTab(self.search_tab, "Tag Search")
#         layout.addWidget(self.tabs, stretch=1)
#         self.plot_widget.addLegend()

#     def filter_tags(self, text):
#         self.tag_list.clear()
#         filtered = [tag for tag in self.all_tags if text.lower() in tag.lower()]
#         self.tag_list.addItems(filtered)

#     def add_tag_plot(self, item):
#         tag = item.text()
#         if tag in self.active_tags:
#             return
#         color = pg.intColor(len(self.active_tags), hues=12)
#         curve = self.plot_widget.plot(pen=pg.mkPen(color, width=2), name=tag)
#         self.active_tags[tag] = (curve, [])

#     def start_timer(self):
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start(1000)

#     def update_plot(self):
#         for tag, (curve, data_list) in self.active_tags.items():
#             value = self.store.finaltag.get(tag, 0)
#             data_list.append(value)
#             if len(data_list) > self.max_points:
#                 data_list[:] = data_list[-self.max_points:]
#             curve.setData(data_list)



# if __name__ == "__main__":
#     import sys
#     import random

#     class FakeStore:
#         def __init__(self):
#             self.finaltag = {
#                 f"Sensor{i}": random.uniform(0, 100) for i in range(1, 21)
#             }
#         def update(self):
#             for key in self.finaltag:
#                 self.finaltag[key] = random.uniform(0, 100)

#     app = QtWidgets.QApplication(sys.argv)
#     store = FakeStore()

#     # شبیه‌سازی آپدیت OPC
#     timer = QtCore.QTimer()
#     timer.timeout.connect(store.update)
#     timer.start(1000)

#     widget = TagPlotWidget(store, list(store.finaltag.keys()))
#     widget.resize(1000, 500)
#     widget.show()

#     sys.exit(app.exec())





from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import os
import sys

class TagPlotWidget(QtWidgets.QWidget):
    def __init__(self, store, all_tags):
        super().__init__()
        self.store = store
        self.setWindowTitle("Multi Trend Window")
        self.all_tags = all_tags
        self.active_tags = {}  # tag: (curve, data_list)
        self.max_points = 100000

        self.init_ui()
        self.start_timer()
    
    def init_ui(self):
        layout = QtWidgets.QHBoxLayout(self)

        # ---- چپ: نمودار ----
        self.plot_widget = pg.PlotWidget(title="multi Trend")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.addLegend()
        layout.addWidget(self.plot_widget, stretch=3)

        # ---- وسط: لیست تگ‌های فعال ----
        self.active_tag_list = QtWidgets.QListWidget()
        self.active_tag_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.active_tag_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.active_tag_list, stretch=1)

        # ---- راست: تب جستجو ----
        self.tabs = QtWidgets.QTabWidget()
        self.search_tab = QtWidgets.QWidget()
        search_layout = QtWidgets.QVBoxLayout()

        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setPlaceholderText("Search..")
        self.search_box.textChanged.connect(self.filter_tags)
        search_layout.addWidget(self.search_box)

        self.tag_list = QtWidgets.QListWidget()
        self.tag_list.addItems(self.all_tags)
        self.tag_list.itemClicked.connect(self.add_tag_plot)
        search_layout.addWidget(self.tag_list)

        self.search_tab.setLayout(search_layout)
        self.tabs.addTab(self.search_tab, "Tag Search")
        layout.addWidget(self.tabs, stretch=1)

    def filter_tags(self, text):
        self.tag_list.clear()
        filtered = [tag for tag in self.all_tags if text.lower() in tag.lower()]
        self.tag_list.addItems(filtered)

    def add_tag_plot(self, item):
        tag = item.text()
        if tag in self.active_tags:
            return
        color = pg.intColor(len(self.active_tags), hues=12)
        curve = self.plot_widget.plot(pen=pg.mkPen(color, width=2), name=tag)
        self.active_tags[tag] = (curve, [])
        self.active_tag_list.addItem(tag)

    def remove_tag_plot(self, item):
        tag = item.text()
        if tag in self.active_tags:
            curve, _ = self.active_tags.pop(tag)
            self.plot_widget.removeItem(curve)
            row = self.active_tag_list.row(item)
            self.active_tag_list.takeItem(row)

    def show_context_menu(self, pos):
        item = self.active_tag_list.itemAt(pos)
        if item:
            menu = QtWidgets.QMenu()
            remove_action = menu.addAction("Remove from Plot")
            action = menu.exec(self.active_tag_list.mapToGlobal(pos))
            if action == remove_action:
                self.remove_tag_plot(item)

    def start_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def setTimer(self,state):
        # if state:
        #     print(state)
        #     self.timer.start(1000)
        # elif state == False:
        #     self.timer.stop()
        pass

    # def update_plot(self):
    #     for tag, (curve, data_list) in self.active_tags.items():
    #         # چک کنیم که history برای این تگ موجود باشه
    #         if tag in self.store.history:
    #             # دوتا لیست جدا کنیم: یکی زمان، یکی مقدار
    #             times, values = zip(*self.store.history[tag])
    #             curve.setData(times, values)  # یا به جای range، خود times رو نرمالایز کن
    #             if self.store.finaltag["420TIMER"] == 0:
    #                 self.plot_widget.removeItem(curve)
    #                 return

    def update_plot(self):
    # اول بررسی کنیم تایمر صفر نباشه
        if self.store.finaltag.get("420TIMER", 0) == 0:
            # همه‌ی curve ها رو پاک کن
            for tag, (curve, _) in list(self.active_tags.items()):
                self.plot_widget.removeItem(curve)
            self.active_tags.clear()   # دیکشنری رو هم خالی کن
            self.active_tag_list.clear()  # لیست سمت راست رو هم خالی کن
            return

        # اگه تایمر غیر صفر بود، دیتا رو بکش
        for tag, (curve, data_list) in self.active_tags.items():
            if tag in self.store.history and self.store.history[tag]:
                times, values = zip(*self.store.history[tag])
                curve.setData(times, values)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    widget = TagPlotWidget()
    widget.resize(1200, 500)
    widget.show()

    sys.exit(app.exec())
