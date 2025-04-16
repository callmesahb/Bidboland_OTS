from PyQt6 import QtWidgets, QtGui, QtCore
from controllerbar import TriangleWidget
from Store import Store
import sys


class ControllerPlate(QtWidgets.QWidget):
    ChangePosValve = QtCore.pyqtSignal(float)
    changeHandtype = QtCore.pyqtSignal(str)
    updatevalues = QtCore.pyqtSignal()

    def __init__(self, name: str, pvvalue: list, variableid, store: Store):
        super().__init__()
        self.name = name
        self.pvvalues = pvvalue
        self.variableid = variableid
        self.store = store
        self.store.updatevalues.connect(self.upandsettingvaluesofcontroller)
        self.setWindowTitle("Controller")
        self.sp_edit_locked = False
        self.sp_edit_lock_timer = QtCore.QTimer(self)
        self.sp_edit_lock_timer.setInterval(3000)
        self.sp_edit_lock_timer.setSingleShot(True)
        self.sp_edit_lock_timer.timeout.connect(self.unlock_sp_edit)
        self.op_edit_locked = False
        self.op_edit_lock_timer = QtCore.QTimer(self)
        self.op_edit_lock_timer.setInterval(3000)
        self.op_edit_lock_timer.setSingleShot(True)
        self.op_edit_lock_timer.timeout.connect(self.unlock_op_edit)

        self.is_editing_op = False
        self.handling_MD = False
        self.is_editing_sp = False
        self._initUI()
        
    def unlock_sp_edit(self):
        self.sp_edit_locked = False
    def unlock_op_edit(self):
        self.op_edit_locked = False


    def _initUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.namee = QtWidgets.QLabel("", self)
        self.namee.setText(str(self.variableid))
        hline = QtWidgets.QFrame()
        self.vlayout.addWidget(self.namee)
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)

        self.settingProgressbar()

    def settingProgressbar(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.Unittag = QtWidgets.QLabel("%", self)
        hlayout.addWidget(self.Unittag)

        self.Progressbar = TriangleWidget()
        self.Progressbar.setminmaxvalue(0, 100)
        hlayout.addWidget(self.Progressbar)

        self.vlayout.addLayout(hlayout)
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)

        self.SettingPlaceVariables()

    def SettingPlaceVariables(self):
        hlayout_sp = QtWidgets.QHBoxLayout()
        self.SP = QtWidgets.QLabel("SP", self)
        self.SPValue = QtWidgets.QLineEdit("", self)
        self.validator = QtGui.QDoubleValidator()
        self.SPValue.setValidator(self.validator)
        self.SPValue.textEdited.connect(self.on_sp_edit_start)
        hlayout_sp.addWidget(self.SP)
        hlayout_sp.addWidget(self.SPValue)
        
        self.SPValue.textEdited.connect(self.on_sp_edit_start)
        self.SPValue.editingFinished.connect(self.on_sp_edit_end)

        hlayout_pv = QtWidgets.QHBoxLayout()
        self.PV = QtWidgets.QLabel("PV", self)
        self.PVValue = QtWidgets.QLineEdit("", self)
        self.PVValue.setReadOnly(True)
        hlayout_pv.addWidget(self.PV)
        hlayout_pv.addWidget(self.PVValue)

        hlayout_op = QtWidgets.QHBoxLayout()
        self.OP = QtWidgets.QLabel("OP(%)", self)
        self.OPValue = QtWidgets.QLineEdit("", self)
        self.OPValue.setReadOnly(True)
        self.OPValue.setValidator(self.validator)
        self.OPValue.textEdited.connect(self.on_op_edit_start)
        self.OPValue.editingFinished.connect(self.on_op_edit_end)


        hlayout_op.addWidget(self.OP)
        hlayout_op.addWidget(self.OPValue)

        hlayout_md = QtWidgets.QHBoxLayout()
        self.MD = QtWidgets.QLabel("MD", self)
        self.MDComboBox = QtWidgets.QComboBox(self)
        self.MDComboBox.addItems(["AUTO","MAN"])
        hlayout_md.addWidget(self.MD)
        hlayout_md.addWidget(self.MDComboBox)

        self.Accept = QtWidgets.QPushButton("APPLY", self)
        self.Accept.clicked.connect(self.UpdateOP)

        self.vlayout.addLayout(hlayout_sp)
        self.vlayout.addLayout(hlayout_pv)
        self.vlayout.addLayout(hlayout_op)
        self.vlayout.addLayout(hlayout_md)
        self.vlayout.addWidget(self.Accept)

        self.setWindowTitle(self.name)
        self.MDComboBox.currentTextChanged.connect(self.handlingmethod)
    def handlingmethod(self):
        Varid = self.variableid.replace("OP", "")
        tv = Varid + "TV"
        # print(self.MDComboBox.currentText())
        if self.MDComboBox.currentText() == "MAN":
            self.store.settingValueOPC(tv,1)
        elif self.MDComboBox.currentText() == "AUTO":
            self.store.settingValueOPC(tv,0)
            
    def on_sp_edit_start(self):
        self.sp_edit_locked = True
        
    def on_op_edit_start(self):
        self.op_edit_locked = True
        
    def on_op_edit_end(self):
        try:
            new_op_value = float(self.OPValue.text())
            self.store.settingValueOPC(self.variableid, new_op_value)
            self.op_edit_lock_timer.start()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "مقدار OP نامعتبر است.")

    def on_op_edit_end(self):
        try:
            new_op_value = float(self.OPValue.text())
            self.store.settingValueOPC(self.variableid, new_op_value)
            self.op_edit_lock_timer.start()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "مقدار OP نامعتبر است.")


    def on_sp_edit_end(self):
        try:
            new_sp_value = float(self.SPValue.text())
            Varid = self.variableid.replace("OP", "")
            sp = Varid + "SP"
            self.store.settingValueOPC(sp, new_sp_value)

            self.sp_edit_lock_timer.start()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "لطفاً عدد معتبر وارد کنید.")

    def UpdateOP(self):
        new_op_value = float(self.OPValue.text())
        self.store.settingValueOPC(self.variableid, new_op_value)

    def ChangingHandType(self):
        new_type = self.MD.text()
        self.changeHandtype.emit(new_type)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Enter or event.key() == QtCore.Qt.Key.Key_Return:
            self.UpdateOP()

    @QtCore.pyqtSlot()
    def upandsettingvaluesofcontroller(self):
        Varid = self.variableid.replace("OP", "")
        sp = Varid + "SP"
        pv = Varid + "PV"
        op = Varid + "OP"
        tv = Varid + "TV"
        opm = Varid + "OPM"
        cas = Varid + "CAS"

        spvalue = self.store.finaltag[sp]
        pvvalue = self.store.finaltag[pv]
        opvalue = self.store.finaltag[op]
        tvvalue = self.store.finaltag[tv]
        casvalue = self.store.finaltag[cas]

        if tvvalue == 1.0:
            self.OPValue.setReadOnly(False)
            self.Accept.setEnabled(True)
        elif tvvalue == 0.0:
            self.OPValue.setReadOnly(True)
            self.Accept.setEnabled(False)
        if casvalue == 1:
            if "CAS" not in [self.MDComboBox.itemText(i) for i in range(self.MDComboBox.count())]:
                self.MDComboBox.addItem("CAS")
        else:
            index = self.MDComboBox.findText("CAS")
            if index >= 0:
                self.MDComboBox.removeItem(index)
        

        # self.SPValue.setText(str(round(spvalue, 2)))
        self.PVValue.setText(str(round(pvvalue, 2)))

        self.Progressbar.progress.setValue(int(opvalue))
        self.Progressbar.setRightValue(int(opvalue))
        if not self.sp_edit_locked:
            self.SPValue.setText(str(round(spvalue, 2)))
        if not self.op_edit_locked:
            self.OPValue.setText(str(round(opvalue, 2)))