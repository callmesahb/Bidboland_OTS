from PyQt6 import QtWidgets, QtGui, QtCore
from ControllerPlateBar import TriangleWidget
from ControllerPage import ControllerPage
from Store import Store
import sys


class ControllerPlate(QtWidgets.QWidget):
    ChangePosValve = QtCore.pyqtSignal(float)
    changeHandtype = QtCore.pyqtSignal(str)
    updatevalues = QtCore.pyqtSignal()
    prdopening = QtCore.pyqtSignal(list)

    def __init__(self, name: str, pvvalue: list, variableid, store: Store,ranges:list,title:str,itype):
        super().__init__()
        self.name = name
        self.pvvalues = pvvalue
        self.variableid = variableid
        self.store = store
        self.ranges = ranges
        self.last_pv_status_when_tv1 = None
        
        self.title = title
        self.itype = itype
        self.setWindowTitle(self.variableid)
        self.setFixedWidth(250)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
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
        self.Varid = self.variableid.replace("OP", "")
        self.unit = self.store.GettingUnit(self.Varid + "PV")
        self.synced_once = False
        self.last_op_value = None
        # print(f"{self.variableid}:{ranges[0]}")
        # self.sp_text = self.store.finaltag["4201FIC047ASP"]
        # self.store.updatevalues.connect(self.updatesptext)
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

        self.namee = QtWidgets.QPushButton("", self)
        title = QtWidgets.QLabel("", self)
        self.namee.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: black;
                text-align: left;
                font-weight:bold;
            }
            QPushButton:hover {
                color: blue;
            }
        """)
        self.namee.clicked.connect(self.printname)
        varid = " " + self.variableid
        self.namee.setText(varid)
        hline = QtWidgets.QFrame()
        titlee = " " + self.title
        self.vlayout.addWidget(self.namee)
        title.setText(titlee)
        self.vlayout.addWidget(title)
        hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vlayout.addWidget(hline)

        self.settingProgressbar()
    def printname(self):
        Varid = self.variableid.replace("OP", "")
        self.contpage = ControllerPage(self.itype,Varid,self.store,self.name,self.pvvalues,self.variableid,self.ranges,self.title)
        # self.contpage.setFixedSize(1200,1200)
        self.contpage.show()
        self.close()
        
    def updatesptext(self):
        sptext = self.store.finaltag["4201FIC047ASP"]
        castext = self.store.finaltag["4201FIC047ACAS"]
        optext = self.store.finaltag["4201TIC047OP"]
        if castext == 1:
            self.store.settingValueOPC("4201FIC047ASP",optext)
            self.synced_once = True
        elif self.synced_once:
            if sptext != self.sp_text and castext == 0:
                self.store.settingValueOPC("4201FIC047ASP",sptext)
                
            
                

    def settingProgressbar(self):
        hlayout = QtWidgets.QHBoxLayout()
        self.Unittag = QtWidgets.QLabel("%", self)
        self.Unittag.setFont(QtGui.QFont("Segoe UI"))
        self.Unittag.setText(self.unit)
        hlayout.addWidget(self.Unittag)
        self.Progressbar = TriangleWidget(self.ranges[2],self.ranges[4],self.ranges[5],self.ranges[3],self.variableid,self.store,self.ranges)
        self.store.updatevalues.connect(self.Progressbar.settingrangesensor)
        self.Progressbar.progress.setFixedHeight(200)
        self.Progressbar.progress.setFixedWidth(30)
        self.Progressbar.rightProgress.setFixedHeight(200)
        self.Progressbar.rightProgress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #efd306;
            }""")
        height = round(self.Progressbar.progress.height(),1)
        step = (height-12) // 4
        self.Progressbar.setFixedHeight(220)
        if self.name[5] == "D":
            self.Progressbar.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            self.Progressbar.label1.setGeometry(self.Progressbar.progress.x()-2, 11, 50, 20)
            self.Progressbar.label2.setGeometry(self.Progressbar.progress.x()-2, 12+step, 50, 20)
            self.Progressbar.label3.setGeometry(self.Progressbar.progress.x()-2, 12+2*step, 50, 20)
            self.Progressbar.label4.setGeometry(self.Progressbar.progress.x()-2,12+3*step, 50, 20)
            self.Progressbar.label5.setGeometry(self.Progressbar.progress.x()-2, 12+4*step, 50, 20)
            self.Progressbar.setminmaxvalue(self.ranges[0], self.ranges[1])
            hlayout.addWidget(self.Progressbar)
        else:
            self.Progressbar.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            self.Progressbar.label1.setGeometry(self.Progressbar.progress.x()-30, 11, 50, 20)
            self.Progressbar.label2.setGeometry(self.Progressbar.progress.x()-30, 12+step, 50, 20)
            self.Progressbar.label3.setGeometry(self.Progressbar.progress.x()-30, 12+2*step, 50, 20)
            self.Progressbar.label4.setGeometry(self.Progressbar.progress.x()-30,12+3*step, 50, 20)
            self.Progressbar.label5.setGeometry(self.Progressbar.progress.x()-28, 12+4*step, 50, 20)
            self.Progressbar.setminmaxvalue(self.ranges[0], self.ranges[1])
            hlayout.addWidget(self.Progressbar)
        
        # self.progress = QtWidgets.QProgressBar()
        # self.progress.setOrientation(QtCore.Qt.Orientation.Vertical)
        # hlayout.addWidget(self.progress)

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
        spacefromend = QtWidgets.QLabel(" ",self)
        self.validator = QtGui.QDoubleValidator()
        self.SPValue.setValidator(self.validator)
        self.SPLine = QtWidgets.QLabel("", self)
        self.SPLine.setStyleSheet("background-color: blue;")
        self.SPLine.setFixedHeight(20)
        self.SPValue.textEdited.connect(self.on_sp_edit_start)
        hlayout_sp.addWidget(spacefromend)
        hlayout_sp.addWidget(self.SP)
        hlayout_sp.addWidget(self.SPLine)
        hlayout_sp.addWidget(self.SPValue)
        hlayout_sp.addWidget(spacefromend)
        hlayout_sp.setSpacing(3)
        
        self.SPValue.textEdited.connect(self.on_sp_edit_start)
        self.SPValue.editingFinished.connect(self.on_sp_edit_end)

        hlayout_pv = QtWidgets.QHBoxLayout()
        self.PV = QtWidgets.QLabel("PV", self)
        self.PVValue = QtWidgets.QLineEdit("", self)
        self.PVLine = QtWidgets.QLabel("", self)
        self.PVLine.setStyleSheet("background-color: #00ff01;")
        self.PVLine.setFixedHeight(20)
        self.PVValue.setReadOnly(True)
        hlayout_pv.addWidget(spacefromend)
        hlayout_pv.addWidget(self.PV)
        hlayout_pv.addWidget(self.PVLine)
        hlayout_pv.addWidget(self.PVValue)
        hlayout_pv.addWidget(spacefromend)
        hlayout_pv.setSpacing(3)

        hlayout_op = QtWidgets.QHBoxLayout()
        self.OP = QtWidgets.QLabel("OP(%)", self)
        self.OPLine = QtWidgets.QLabel("", self)
        self.OPLine.setStyleSheet("background-color: #efd306;")
        self.OPLine.setFixedHeight(20)
        self.OPValue = QtWidgets.QLineEdit("", self)
        self.OPValue.setReadOnly(True)
        self.OPValue.setValidator(self.validator)
        self.OPValue.textEdited.connect(self.on_op_edit_start)
        self.OPValue.editingFinished.connect(self.on_op_edit_end)

        hlayout_op.addWidget(spacefromend)
        hlayout_op.addWidget(self.OP)
        hlayout_op.addWidget(self.OPLine)
        hlayout_op.addWidget(self.OPValue)
        hlayout_op.addWidget(spacefromend)
        hlayout_op.setSpacing(3)

        hlayout_md = QtWidgets.QHBoxLayout()
        self.MD = QtWidgets.QLabel(" MD", self)
        self.MDComboBox = QtWidgets.QComboBox(self)
        # self.MDComboBox.addItems(["AUTO","MAN"])
        # hlayout_md.addWidget(spacefromend)
        hlayout_md.addWidget(self.MD)
        hlayout_md.addWidget(self.MDComboBox)
        hlayout_md.addWidget(spacefromend)
        hlayout_md.setSpacing(0)

        hlayout_btn = QtWidgets.QHBoxLayout()
        self.Accept = QtWidgets.QPushButton("APPLY", self)
        hlayout_btn.addWidget(spacefromend)
        hlayout_btn.addWidget(self.Accept)
        hlayout_btn.addWidget(spacefromend)
        hlayout_btn.setSpacing(3)
        self.Accept.clicked.connect(self.UpdateOP)

        self.vlayout.addLayout(hlayout_sp)
        self.vlayout.addLayout(hlayout_pv)
        self.vlayout.addLayout(hlayout_op)
        self.vlayout.addLayout(hlayout_md)
        self.vlayout.addLayout(hlayout_btn)
        # self.vlayout.addWidget(self.Accept)

        self.setWindowTitle(self.name)
        self.MDComboBox.currentTextChanged.connect(self.handlingmethod)
    def handlingmethod(self):
        Varid = self.variableid.replace("OP", "")
        tv = Varid + "TV"
        prd = Varid + "PRD"
        cas = Varid + "CAS"
        ctam = "4201FIC047ACTAM"
        # self.saved_mode = self.store.finaltag["4201FIC047"]
        # ctamvalue = self.store.finaltag["4201FIC047ACTAM"]
        # print(self.MDComboBox.currentText())
        if self.MDComboBox.currentText() == "MAN":
            self.store.settingValueOPC(tv,1)
            self.store.settingValueOPC(prd,1)
            self.store.settingValueOPC(cas,0)
        elif self.MDComboBox.currentText() == "AUTO":
            self.store.settingValueOPC(tv,0)
            self.store.settingValueOPC(prd,1)
            self.store.settingValueOPC(cas,0)
        elif self.MDComboBox.currentText() == "CAS":
            self.store.settingValueOPC(tv,0)
            self.store.settingValueOPC(prd,0)
            self.store.settingValueOPC(cas,1)
        elif self.MDComboBox.currentText() == "PRD":
            self.store.settingValueOPC(tv,0)
            self.store.settingValueOPC(prd,2)
            self.store.settingValueOPC(cas,0)
            
    def on_sp_edit_start(self):
        self.sp_edit_locked = True
        
    def on_op_edit_start(self):
        self.op_edit_locked = True
        
    def on_op_edit_end(self):
        try:
            new_op_value = float(self.OPValue.text())
            new_sp_value = float(self.SPValue.text())
            op = self.variableid + "OP"
            sp = self.variableid + "SP"
            self.store.settingValueOPC(op, new_op_value)
            self.store.settingValueOPC(sp, new_sp_value)
            self.op_edit_lock_timer.start()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "مقدار OP نامعتبر است.")

    def on_op_edit_end(self):
        try:
            new_op_value = float(self.OPValue.text())
            op = self.variableid + "OP"
            self.store.settingValueOPC(op, new_op_value)
            self.op_edit_lock_timer.start()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "مقدار OP نامعتبر است.")


    def on_sp_edit_end(self):
        try:
            new_sp_value = float(self.SPValue.text())
            # Varid = self.variableid.replace("OP", "")
            sp = self.variableid + "SP"
            pv = self.variableid + "PV"
            if new_sp_value >= self.ranges[1] :
                new_sp_value = self.ranges[1]
            elif new_sp_value <= self.ranges[0]:
                new_sp_value = self.ranges[0]
            else:
                new_sp_value = new_sp_value
            self.store.settingValueOPC(sp, new_sp_value)

            self.sp_edit_lock_timer.start()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "خطا", "لطفاً عدد معتبر وارد کنید.")

    def UpdateOP(self):
        new_op_value = float(self.OPValue.text())
        # print(new_op_value)
        varid = self.variableid + "OPM"
        self.store.settingValueOPC(varid, new_op_value)

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
        prd = Varid + "PRD"
        pvl = Varid + "PVL"
        pvh = Varid + "PVH"
        pvlv = self.store.finaltag[pvl]
        pvhv = self.store.finaltag[pvh]
        # ctamvalue = self.store.finaltag["4201FIC047ACTAM"]
        
        # self.MDComboBox.clear()
        
        spvalue = self.store.finaltag[sp]
        pvvalue = self.store.finaltag[pv]
        opvalue = self.store.finaltag[op]
        # if op == "4201LIC021BOP":
        #     print(f"{op}:{opvalue}")
        # if opvalue >= 100:
        #     opvalue = 100
        # elif opvalue <= 0:
        #     opvalue = 0
        tvvalue = self.store.finaltag[tv]
        casvalue = self.store.finaltag[cas]
        if pvvalue <= self.ranges[0]:
            pvvalue = self.ranges[0]
        elif pvvalue >= self.ranges[1]:
            pvvalue = self.ranges[1]
        target_items = []
        current_items = [self.MDComboBox.itemText(i) for i in range(self.MDComboBox.count())]
        
        if self.name == "0TIC015":
            prdvalue = self.store.finaltag[prd]
            target_items = ["AUTO","MAN","PRD"]
            if prdvalue == 2:
                opvalueprd = self.store.finaltag["407ES0TIC015OP"]
                self.prdopening.emit(["407ES0FIC015OP",opvalueprd,True])
                target_items = ["PRD","AUTO","MAN"]
            elif prdvalue == 1:
                opvalueprd = self.store.finaltag["407ES0FIC015OP"]
                self.prdopening.emit(["407ES0FIC015OP",opvalueprd,False])
                target_items = ["AUTO","MAN","PRD"]
                
        else:
            if self.name == "0FIC015":
                optext = self.store.finaltag["407ES0TIC015OP"]
                target_items = ["CAS","AUTO","MAN"]
                # self.store.settingValueOPC("4201FIC047ACAS",1)
                self.last_op_value = optext
                tvvalue = self.store.finaltag["407ES0FIC015TV"]
                # target_items = ["AUTO", "MAN", "CAS"]
                
                    # target_items = ["AUTO", "MAN", "CAS"]
                if casvalue == 1 and tvvalue == 0:
                    spvalue = self.store.finaltag["407ES0TIC015OP"]
                    self.store.settingValueOPC("407ES0FIC015SP",spvalue)
                elif casvalue == 0 and tvvalue == 1:
                    target_items = ["MAN","AUTO","CAS"]
                    if not self.synced_once:
                        self.store.settingValueOPC("407ES0FIC015SP",self.last_op_value)
                        self.synced_once = True
                    spvalue = self.store.finaltag["407ES0FIC015SP"]
                elif casvalue == 0 and tvvalue == 0:
                    target_items = ["AUTO","MAN","CAS"]
                    # elif ctamvalue == 0:
                    #     target_items = ["CAS","AUTO","MAN"]
                    # if tvvalue == 0:
                    #     target_items = ["AUTO","MAN","CAS"]
                    # elif tvvalue == 0 and casvalue == 0:
                    #     target_items = ["AUTO","MAN","CAS"]
                    # self.store.settingValueOPC(cas,0)
                    # if not self.synced_once:
                    #     self.store.settingValueOPC("4201FIC047ASP",self.last_op_value)
                    #     self.synced_once = True
                        # if self.last_op_value != self.sp_text:
                        #     print("KIRRR")
                        #     self.store.settingValueOPC("4201FIC047ASP",self.sp_text)
                    spvalue = self.store.finaltag["407ES0FIC015SP"]
            elif tvvalue == 1:
                target_items = ["MAN", "AUTO"]
            elif tvvalue == 0:
                # showspvalue = spvalue
                target_items = ["AUTO", "MAN"]

            
        for item in current_items:
            if item not in target_items:
                index = self.MDComboBox.findText(item)
                if index >= 0:
                    self.MDComboBox.removeItem(index)
        
        for item in target_items:
            if item not in current_items:
                self.MDComboBox.addItem(item)

        if tvvalue == 1.0:
            self.OPValue.setReadOnly(False)
            self.Accept.setEnabled(True)
        #     self.MDComboBox.addItems(["MAN","AUTO"])
        #     manindex = self.MDComboBox.findText("MAN")
        #     autindex = self.MDComboBox.findText("AUTO")
        #     if manindex >= 0 or autindex >= 0:
        #         self.MDComboBox.removeItem(manindex)
        #         self.MDComboBox.removeItem(autindex)
        elif tvvalue == 0.0:
            self.OPValue.setReadOnly(True)
            self.Accept.setEnabled(False)
        #     self.MDComboBox.addItems(["AUTO","MAN"])
        #     manindex = self.MDComboBox.findText("MAN")
        #     autindex = self.MDComboBox.findText("AUTO")
            
        # if casvalue == 1:
        #     if "CAS" not in [self.MDComboBox.itemText(i) for i in range(self.MDComboBox.count())]:
        #         self.MDComboBox.addItems(["CAS","AUTO"])
        # else:
        #     index = self.MDComboBox.findText("CAS")
        #     manindex = self.MDComboBox.findText("MAN")
        #     autindex = self.MDComboBox.findText("AUTO")
        #     if index >= 0:
        #         self.MDComboBox.removeItem(index)
        #     elif manindex >=0:
        #         self.MDComboBox.removeItem(manindex)
        #     elif autindex >=0:
        #         self.MDComboBox.removeItem(autindex)
        

        # self.SPValue.setText(str(round(spvalue, 2)))
        self.PVValue.setText(str(round(pvvalue, 2)))
        self.fvalue = self.Progressbar.value_to_percent(pvvalue)
        self.Progressbar.progress.setValue(int(self.fvalue))
        self.Progressbar.setLeftValue(spvalue)
        self.Progressbar.rightProgress.setValue(int(opvalue))
        # self.Progressbar.setRightValue(int(pvvalue))
        if pvvalue < pvlv and pvvalue > self.ranges[0]:
            self.Progressbar.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #fffc00;
            }
        """)
        elif pvvalue >= pvhv and pvvalue < self.ranges[1]:
            self.Progressbar.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    background-color: black;
                    border-radius: 5px;
                }
                QProgressBar::chunk {
                    background-color: #fffc00;
                }
            """)
        elif pvvalue > pvlv and pvvalue < pvhv:
            self.Progressbar.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: rgb(0,255,1);
            }
        """)
        elif pvvalue == self.ranges[3] :
            self.Progressbar.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                background-color: black;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: rgb(255,255,1);
            }
        """)
        if not self.sp_edit_locked:
            self.SPValue.setText(str(round(spvalue, 2)))
        if not self.op_edit_locked:
            self.OPValue.setText(str(round(opvalue, 2)))
        self.update()