from PyQt6 import QtCore


class SignalBus(QtCore.QObject):
    reset_all_trends = QtCore.pyqtSignal(bool)
    def __init__(self):
        super().__init__()