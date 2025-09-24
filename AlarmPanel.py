from PyQt6 import QtWidgets, QtGui, QtCore
from controllerbar import TriangleWidget
from Store import Store
from Trend import Trend
from AlarmPagePlate import Sensor
import sys
import os

class AlarmPanel(QtWidgets.QWidget):
    def __init__(self,type,variableid,store:Store,ranges,name,title):
        super().__init__()
        self.type = type
        self.variableid = variableid
        self.store = store
        self.ranges = ranges
        self.name = name
        self.title = title
        self.contplate = Sensor(store,name,variableid,ranges,title,type)
        # self.contplate.pvstatus.connect(self.changestatusofalarm)
        self._initUI()
    def _initUI(self):
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.addWidget(self.contplate)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(MainTab(self.store,self.name,self.variableid,self.ranges,self.title,self.type),"Main")
        self.tabs.addTab(Alarms(self.store,self.name,self.variableid,self.ranges,self.title,self.type),"Alarms")
        self.tabs.addTab(Chart(self.type,self.variableid,self.store,self.ranges),"Chart")
        # self.tabs.addTab(Alarms(self.variableid,self.store,self.name,self.pvvalues,self.ranges,self.itype,self.title),"Alarms")
        # self.tabs.addTab(Chart(self.itype,self.variableid,self.store),"Chart")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.hlayout.addLayout(main_layout)
        self.setLayout(self.hlayout)
        
class MainTab(QtWidgets.QWidget):
    def __init__(self,store,name,variableid,ranges,title,type):
        super().__init__()
        self.contplate = Sensor(store,name,variableid,ranges,title,type)
        self.contplate.pvstatus.connect(self.changestatusofalarm)
        self.fontt = QtGui.QFont("New Times Roman")
        # self.store = store
        # self.variableid = variableid
        self.fontt.setBold(True)
        self.ranges = ranges
        self.font2 = QtGui.QFont("New Times Roman")
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.getvalue)
        # self.timer.start(1000)
        
        self.InitUI()
    @QtCore.pyqtSlot(str)
    def changestatusofalarm(self,status:str):
        if status == "LL ALARM":
            self.pvradiolowlowvalue.setChecked(True)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.moduleradio.setChecked(True)
            self.moduleradio.setText("ON")
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("ON")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
        if status == "HH ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(True)
            self.pvradiolowvalue.setChecked(False)
            self.moduleradio.setChecked(True)
            self.moduleradio.setText("ON")
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("ON")
            self.pvradiohighvalue.setText("OFF")
        if status == "H ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(True)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.moduleradio.setChecked(True)
            self.moduleradio.setText("ON")
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("ON")
        if status == "L ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(True)
            self.moduleradio.setChecked(True)
            self.moduleradio.setText("ON")
            self.pvradiolowvalue.setText("ON")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
            
        if status == "NORMAL":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.moduleradio.setChecked(False)
            self.moduleradio.setText("OFF")
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
    def InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.vlayout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vlayout2 = QtWidgets.QVBoxLayout()
        self.vlayout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.execandcontrol()
        
        
    def execandcontrol(self):
        g1layout = QtWidgets.QGridLayout()
        titlelabel = QtWidgets.QLabel("Execution and control")
        titlelabel.setFont(self.fontt)
        g1layout.addWidget(titlelabel,0,0)
        g1layout.addWidget(QtWidgets.QLabel("Execution State:"),1,0)
        var1 = QtWidgets.QLineEdit("ACTIVE")
        var1.setEnabled(False)
        var1.setFixedSize(100,25)
        var1.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        var1.setReadOnly(True)
        g1layout.addWidget(var1,1,1)
        g1layout.addWidget(QtWidgets.QLabel("Load State:"),2,0)
        state = QtWidgets.QLabel("RUN")
        state.setStyleSheet("color:gray;")
        g1layout.addWidget(state,2,1)
        g1layout.addWidget(QtWidgets.QLabel("Order in CEE:"),3,0)
        g1layout.addWidget(QtWidgets.QLabel("Execution Period:"),4,0)
        g1layout.addWidget(QtWidgets.QLabel("Execution Phase:"),5,0)
        g1layout.addWidget(QtWidgets.QLabel("Control Level:"),6,0)
        checked = QtWidgets.QCheckBox("Control Configuration")
        checked.setEnabled(False)
        g1layout.addWidget(checked,7,0,1,2)
        self.vlayout1.addLayout(g1layout)
        self.ProcessVariable()
        
    def ProcessVariable(self):
        g2layout = QtWidgets.QGridLayout()
        font = QtGui.QFont("Arial")
        font.setBold(True)
        title = QtWidgets.QLabel("Process variable")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        # highvalue = self.store.SettingDetailsofsensor(varid)[1]
        # lowvalue = self.store.SettingDetailsofsensor(varid)[0]
        # pvhighrange = QtWidgets.QLabel(str(highvalue))
        # pvhighrange.setFont(font)
        # pvlowrange = QtWidgets.QLabel(str(lowvalue))
        # pvlowrange.setFont(font)
        # g2layout.addWidget(pvhighrange,1,1)
        # g2layout.addWidget(pvlowrange,2,1)
        g2layout.addWidget(QtWidgets.QLabel("PV characterization:DACA"),1,0)
        g2layout.addWidget(QtWidgets.QLabel("LINEAR"),1,1)
        g2layout.addWidget(QtWidgets.QLabel("PV status:DACA"),2,0)
        g2layout.addWidget(QtWidgets.QLabel("NORMAL"),2,1)
        g2layout.addWidget(QtWidgets.QLabel("PV source option:DACA"),3,0)
        pvsourceoption = QtWidgets.QComboBox()
        pvsourceoption.addItem("ALL")
        pvsourceoption.setEnabled(False)
        g2layout.addWidget(pvsourceoption,3,1)
        g2layout.addWidget(QtWidgets.QLabel("PV source:DACA"),4,0)
        pvsource = QtWidgets.QComboBox()
        pvsource.addItem("AUTO")
        pvsource.setEnabled(False)
        g2layout.addWidget(pvsource,4,1)
        g2layout.addWidget(QtWidgets.QLabel("PV high limit(EU):"),9,0)
        
        
        highvalue = self.ranges[1]
        lowvalue = self.ranges[0]
        pvhighlimitvalue = highvalue + 0.03*highvalue
        pvlowlimitvalue = lowvalue - 0.03 * lowvalue
        
        pvhighvalue = QtWidgets.QLabel("",self)
        pvhighvalue.setFont(self.fontt)
        pvhighvalue.setText(str(highvalue))
        g2layout.addWidget(pvhighvalue,7,1)
        
        
        pvlow = QtWidgets.QLabel("",self)
        pvlow.setFont(self.fontt)
        pvlow.setText(str(lowvalue))
        g2layout.addWidget(pvlow,8,1)
        
        
        pvhighlimit = QtWidgets.QLabel("5660",self)
        pvhighlimit.setFont(self.fontt)
        pvhighlimit.setText(str(pvhighlimitvalue))
        g2layout.addWidget(pvhighlimit,9,1)
        
        
        pvlowlimit = QtWidgets.QLabel("-160",self)
        pvlowlimit.setFont(self.fontt)
        pvlowlimit.setText(str(pvlowlimitvalue))
        g2layout.addWidget(pvlowlimit,10,1)
        
        
        # pvhighlimit = QtWidgets.QLabel(str(pvhighlimitvalue))
        # pvhighlimit.setFont(font)
        # g2layout.addWidget(pvhighlimit,9,1)
        # pvhighrange = QtWidgets.QLabel(str(highvalue))
        # pvhighrange.setFont(font)
        # g2layout.addWidget(pvhighrange,10,1)
        g2layout.addWidget(QtWidgets.QLabel("PV high range(EU):"),7,0)
        g2layout.addWidget(QtWidgets.QLabel("PV low range(EU):"),8,0)
        # pvlowrangevalue = QtWidgets.QLabel(str(lowvalue))
        # pvlowrangevalue.setFont(font)
        # g2layout.addWidget(pvlowrangevalue,11,1)
        # pvlowlimitvalue = lowvalue - 0.03 * lowvalue
        # pvlowlimit = QtWidgets.QLabel(str(pvlowlimitvalue))
        # pvlowlimit.setFont(font)
        # g2layout.addWidget(pvlowlimit,12,1)
        g2layout.addWidget(QtWidgets.QLabel("PV low limit(EU):"),10,0)
        self.vlayout1.addLayout(g2layout)
        self.Clamping()
        # self.setLayout(self.vlayout1)
        
    def Clamping(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Clamping/Filtering")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        g2layout.addWidget(QtWidgets.QLabel("Input clamping option:DACA"),1,0)
        g2layout.addWidget(QtWidgets.QLabel("Filter time(minutes):DACA"),2,0)
        g2layout.addWidget(QtWidgets.QLabel("Low signal cutoff:DACA"),3,0)
        combo1 = QtWidgets.QComboBox()
        combo1.setFixedSize(200,25)
        combo1.addItem("Disabled")
        combo1.setEnabled(False)
        g2layout.addWidget(combo1,1,1)
        line1 = QtWidgets.QLineEdit("NaN")
        line1.setFixedSize(200,25)
        line1.setEnabled(False)
        g2layout.addWidget(line1,2,1,QtCore.Qt.AlignmentFlag.AlignLeft)
        line2 = QtWidgets.QLineEdit("NaN")
        line2.setFixedSize(200,25)
        line2.setEnabled(False)
        g2layout.addWidget(line2,3,1)
        self.vlayout1.addLayout(g2layout)
        self.alarmenableandsummary()
        
    def alarmenableandsummary(self):
        g5layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Alarm enable and summary")
        title.setFont(self.fontt)
        g5layout.addWidget(title,0,0)
        enblingalarm = QtWidgets.QCheckBox("Enabling Alarm")
        enblingalarm.setChecked(True)
        # enblingalarm.setCheckable(False)
        journal = QtWidgets.QCheckBox("Journal only option")
        journal.setEnabled(False)
        controlmodulecheck = QtWidgets.QCheckBox("OFF")
        controlmodulecheck.setChecked(False)
        controlmodulecheck.setCheckable(False)
        enblingalarm.setEnabled(False)
        g5layout.addWidget(enblingalarm,1,0)
        g5layout.addWidget(journal,2,0)
        g5layout.addWidget(QtWidgets.QLabel("Control module in alarm:"),3,0)
        g5layout.addWidget(QtWidgets.QLabel("PV high-high:"),4,0)
        self.moduleradio = QtWidgets.QRadioButton("OFF")
        self.moduleradio.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g5layout.addWidget(self.moduleradio,3,1)
        self.pvradiohighhighvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiohighhighvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g5layout.addWidget(self.pvradiohighhighvalue,4,1)
        g5layout.addWidget(QtWidgets.QLabel("PV high:"),5,0)
        self.pvradiohighvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiohighvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g5layout.addWidget(self.pvradiohighvalue,5,1)
        g5layout.addWidget(QtWidgets.QLabel("PV low:"),6,0)
        self.pvradiolowvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiolowvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g5layout.addWidget(self.pvradiolowvalue,6,1)
        g5layout.addWidget(QtWidgets.QLabel("PV low-low:"),7,0)
        self.pvradiolowlowvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiolowlowvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g5layout.addWidget(self.pvradiolowlowvalue,7,1)
        g5layout.addWidget(QtWidgets.QLabel("Positive rate of change:"),8,0)
        g5layout.addWidget(QtWidgets.QLabel("Negative rate of change:"),9,0)
        g5layout.addWidget(QtWidgets.QLabel("Bad PV:"),10,0)
        # g5layout.addWidget(controlmodulecheck,3,1)
        # g5layout.addWidget(controlmodulecheck,4,1)
        # g5layout.addWidget(controlmodulecheck,5,1)
        # g5layout.addWidget(controlmodulecheck,6,1)
        # g5layout.addWidget(controlmodulecheck,7,1)
        for row in [8,9,10]:
            pvradiolowlowvalue1 = QtWidgets.QRadioButton("OFF")
            pvradiolowlowvalue1.setCheckable(False)
            pvradiolowlowvalue1.setStyleSheet("""
                    QRadioButton::indicator {
                        background-color: red;
                        border: 1px solid gray;
                        width: 15px;
                        height: 15px;
                        border-radius: 7px;
                    }
                    QRadioButton::indicator:checked {
                        background-color: red;
                    }
                    QRadioButton::indicator:unchecked {
                        background-color: black;
                    }
                    """)
            g5layout.addWidget(pvradiolowlowvalue1,row,1)
        self.radiogroup = QtWidgets.QButtonGroup(self)
        self.radiogroup.setExclusive(False)
        self.radiogroup.addButton(self.pvradiohighvalue)
        self.radiogroup.addButton(self.pvradiohighhighvalue)
        self.radiogroup.addButton(self.pvradiolowvalue)
        self.radiogroup.addButton(self.pvradiolowlowvalue)
        # self.vlayout1.addLayout(g6layout)
        self.radiogroup.addButton(self.moduleradio)
        self.vlayout2.addLayout(g5layout)
        self.QVCs()
        
    def QVCs(self):
        g8layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("QVCS imformation")
        title.setFont(self.fontt)
        g8layout.addWidget(title,0,0)
        g8layout.addWidget(QtWidgets.QLabel("Qualification state:"),1,0)
        text = QtWidgets.QLabel("<None>")
        version = QtWidgets.QLabel("0.00")
        version.setStyleSheet("color:gray;")
        text.setStyleSheet("color:gray;")
        g8layout.addWidget(text,1,1)
        g8layout.addWidget(QtWidgets.QLabel("Version:"),2,0)
        g8layout.addWidget(version,2,1)
        self.vlayout2.addLayout(g8layout)
        # self.setLayout(self.vlayout2)
        self.assignedcontroller()
        
    def assignedcontroller(self):
        g4layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Assigned controller")
        title.setFont(self.fontt)
        g4layout.addWidget(title,0,0)
        g4layout.addWidget(QtWidgets.QLabel("Controller name:"),1,0)
        g4layout.addWidget(QtWidgets.QLabel("Execution environment:"),2,0)
        self.vlayout1.addLayout(g4layout)
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.setStretch(0,1)
        self.hlayout.setStretch(1,1)
        self.setLayout(self.hlayout)
        
        
class Alarms(QtWidgets.QWidget):
    def __init__(self,store,name,variableid,ranges,title,type):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.store = store
        self.variableid = variableid
        self.ranges = ranges
        self.pvll = self.variableid + "PVLL"
        self.pvl = self.variableid + "PVL"
        self.pvh = self.variableid + "PVH"
        self.pvhh = self.variableid + "PVHH"
        self.pvllv = self.store.finaltag[self.pvll]
        self.pvlv = self.store.finaltag[self.pvl]
        self.pvhv = self.store.finaltag[self.pvh]
        self.pvhhv = self.store.finaltag[self.pvhh]
        self.contplate = Sensor(store,name,variableid,ranges,title,type)
        self.contplate.pvstatus.connect(self.changestatusofalarm)
        self._initUI()
    
    def _initUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setSpacing(5)
        # self.vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.Alarmconf()
        
    def Alarmconf(self):
        g1layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Alarm configuration")
        title.setFont(self.fontt)
        g1layout.addWidget(title,0,0)
        type = QtWidgets.QLabel("Type")
        type.setFont(self.fontt)
        g1layout.addWidget(type,1,0)
        Status = QtWidgets.QLabel("Status")
        Status.setFont(self.fontt)
        g1layout.addWidget(Status,1,1)
        Block = QtWidgets.QLabel("Block")
        Block.setFont(self.fontt)
        g1layout.addWidget(Block,1,2)
        Trip_point = QtWidgets.QLabel("Trip point")
        Trip_point.setFont(self.fontt)
        g1layout.addWidget(Trip_point,1,3)
        Priority = QtWidgets.QLabel("Priority")
        Priority.setFont(self.fontt)
        g1layout.addWidget(Priority,1,4)
        Severity = QtWidgets.QLabel("Severity")
        Severity.setFont(self.fontt)
        g1layout.addWidget(Severity,1,5)
        Ondelaytime = QtWidgets.QLabel("On-Delay\ntime(Sec)")
        Ondelaytime.setFont(self.fontt)
        g1layout.addWidget(Ondelaytime,1,6)
        offdelaytime = QtWidgets.QLabel("Off-Delay\ntime(Sec)")
        offdelaytime.setFont(self.fontt)
        g1layout.addWidget(offdelaytime,1,7)
        deadboundvalue = QtWidgets.QLabel("Deadband\n  value")
        deadboundvalue.setFont(self.fontt)
        g1layout.addWidget(deadboundvalue,1,8)
        Deadbandunits = QtWidgets.QLabel("Deadband\n  units")
        Deadbandunits.setFont(self.fontt)
        g1layout.addWidget(Deadbandunits,1,9)
        
        g1layout.addWidget(QtWidgets.QLabel("PV high-high:"),2,0)
        self.pvradiohighhighvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiohighhighvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g1layout.addWidget(self.pvradiohighhighvalue,2,1)
        g1layout.addWidget(QtWidgets.QLabel("PV high:"),3,0)
        self.pvradiohighvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiohighvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g1layout.addWidget(self.pvradiohighvalue,3,1)
        g1layout.addWidget(QtWidgets.QLabel("PV low:"),4,0)
        self.pvradiolowvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiolowvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g1layout.addWidget(self.pvradiolowvalue,4,1)
        g1layout.addWidget(QtWidgets.QLabel("PV low-low:"),5,0)
        self.pvradiolowlowvalue = QtWidgets.QRadioButton("OFF")
        self.pvradiolowlowvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: red;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        g1layout.addWidget(self.pvradiolowlowvalue,5,1)
        g1layout.addWidget(QtWidgets.QLabel("Positive rate of change:"),6,0)
        g1layout.addWidget(QtWidgets.QLabel("Negative rate of change:"),7,0)
        g1layout.addWidget(QtWidgets.QLabel("Bad PV:"),8,0)
        for i in [6,7,8]:
            nothing = QtWidgets.QRadioButton("OFF")
            nothing.setCheckable(False)
            nothing.setStyleSheet("""
                    QRadioButton::indicator {
                        background-color: red;
                        border: 1px solid gray;
                        width: 15px;
                        height: 15px;
                        border-radius: 7px;
                    }
                    QRadioButton::indicator:checked {
                        background-color: red;
                    }
                    QRadioButton::indicator:unchecked {
                        background-color: black;
                    }
                    """)
            g1layout.addWidget(nothing,i,1)
        for i in range(2,9):
            g1layout.addWidget(QtWidgets.QLabel("DACA"),i,2)
            c = QtWidgets.QLineEdit("0")
            c.setEnabled(False)
            c1 = QtWidgets.QLineEdit("0")
            c1.setEnabled(False)
            c2 = QtWidgets.QLineEdit("0")
            c2.setEnabled(False)
            g1layout.addWidget(c,i,5)
            g1layout.addWidget(c1,i,6)
            g1layout.addWidget(c2,i,7)
            
        self.pvhighhighvalue = QtWidgets.QLineEdit()
        g1layout.addWidget(self.pvhighhighvalue,2,3)
        self.pvhighhighvalue.setText(str(self.pvhhv))
        self.pvhighhighvalue.returnPressed.connect(self.changingvalue)
        self.pvhighvalue = QtWidgets.QLineEdit()
        # if self.pvhhv == self.pvhv:
        #     self.pvhighvalue.setText(str(self.pvhhv))
        # else:
        #     self.pvhighhighvalue.setText(str(self.pvhv))
        self.pvhighvalue.setText(str(self.pvhv))
        self.pvhighvalue.returnPressed.connect(self.changingvalue)
        g1layout.addWidget(self.pvhighvalue,3,3)
        self.pvlowvalue = QtWidgets.QLineEdit()
        self.pvlowvalue.setText(str(self.pvlv))
        # if self.pvllv == self.pvlv:
        #     self.pvhighhighvalue.setText(str(self.pvllv))
        # else:
        #     self.pvhighhighvalue.setText(str(self.pvlv))
        self.pvlowvalue.returnPressed.connect(self.changingvalue)
        g1layout.addWidget(self.pvlowvalue,4,3)
        self.pvlowlowvalue = QtWidgets.QLineEdit()
        self.pvlowlowvalue.setText(str(self.pvllv))
        self.pvlowlowvalue.returnPressed.connect(self.changingvalue)
        g1layout.addWidget(self.pvlowlowvalue,5,3)
        for i in range(6,8):
            if i == 8:
                continue
            l = QtWidgets.QLineEdit("NaN")
            l.setEnabled(False)
            g1layout.addWidget(l,i,3)
        for i in [2,5]:
            c = QtWidgets.QComboBox()
            c.addItem("HIGH")
            c.setEnabled(False)
            g1layout.addWidget(c,i,4)
        for i in [3,4,6,7]:
            c = QtWidgets.QComboBox()
            c.addItem("LOW")
            c.setEnabled(False)
            g1layout.addWidget(c,i,4)
        for i in [2,3,4,5]:
            d = QtWidgets.QLineEdit("2")
            d.setEnabled(False)
            g1layout.addWidget(d,i,8)
        for i in [2,3,4,5]:
            d = QtWidgets.QLineEdit("2")
            d.setEnabled(False)
            g1layout.addWidget(d,i,8)
            radiobtn = QtWidgets.QRadioButton("%")
            radiobtn.setChecked(False)
            radiobtn.setEnabled(False)
            g1layout.addWidget(radiobtn,i,9)
            radiobtn1 = QtWidgets.QRadioButton("EU")
            radiobtn1.setChecked(True)
            radiobtn1.setEnabled(False)
            g1layout.addWidget(radiobtn1,i,10)
        # for i in range(2,14):
        #     if i in [6,7,8]:
        #         continue
            
        cd = QtWidgets.QComboBox()
        cd.addItem("URGENT")
        cd.setEnabled(False)
        g1layout.addWidget(cd,8,4)
        g1layout.addWidget(self.pvradiolowvalue,2,1)
        self.radiogroup = QtWidgets.QButtonGroup(self)
        self.radiogroup.setExclusive(False)
        self.radiogroup.addButton(self.pvradiohighhighvalue)
        self.radiogroup.addButton(self.pvradiohighvalue)
        self.radiogroup.addButton(self.pvradiolowvalue)
        self.radiogroup.addButton(self.pvradiolowlowvalue)
        self.vlayout.addLayout(g1layout)
        self.DACAblockoption()
        
    def changingvalue(self):
        pvh = self.variableid + "PVH"
        pvhh = self.variableid + "PVHH"
        pvl = self.variableid + "PVL"
        pvll = self.variableid + "PVLL"
        pvhhv = self.pvhighhighvalue.text()
        pvhv = self.pvhighvalue.text()
        pvlv = self.pvlowvalue.text()
        pvllv = self.pvlowlowvalue.text()
        
        if float(pvhhv) > self.ranges[1]:
            pvhhv = self.ranges[1]
        elif float(pvhv) > self.ranges[1]:
            pvhv = self.ranges[1]
        elif float(pvlv) < self.ranges[0]:
            pvlv = self.ranges[0]
        elif float(pvllv) < self.ranges[0]:
            pvllv = self.ranges[0]
        self.pvlowvalue.setText(str(pvlv))
        self.pvlowlowvalue.setText(str(pvllv))
        self.pvhighvalue.setText(str(pvhv))
        self.pvhighhighvalue.setText(str(pvhhv))
        self.store.settingValueOPC(pvh,pvhv)
        self.store.settingValueOPC(pvhh,pvhhv)
        self.store.settingValueOPC(pvl,pvlv)
        self.store.settingValueOPC(pvll,pvllv)
        # floatpvhhv = float(pvhhv)
        # floatpvhv = float(pvhv)
        # floatpvl = float(pvlv)
        # floatpvll = float(pvllv)
        # if floatpvhhv == floatpvhv:
        #     self.store.settingValueOPC(pvh,floatpvhhv)
        # elif floatpvl == floatpvll:
        #     self.store.settingValueOPC(pvl,floatpvll)
        
    def DACAblockoption(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("DACA block options")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        g2layout.addWidget(QtWidgets.QLabel("Significant change:"),1,0)
        g2layout.addWidget(QtWidgets.QLabel("         Low:"),2,0)
        line1 = QtWidgets.QLineEdit("NaN")
        line1.setEnabled(False)
        line1.setFixedSize(100,25)
        g2layout.addWidget(line1,2,1,QtCore.Qt.AlignmentFlag.AlignLeft)
        g2layout.addWidget(QtWidgets.QLabel("         High:"),2,2)
        line2 = QtWidgets.QLineEdit("NaN")
        line2.setEnabled(False)
        line2.setFixedSize(100,25)
        g2layout.addWidget(line2,2,3)
        self.vlayout.addLayout(g2layout)
        self.setLayout(self.vlayout)
        
    @QtCore.pyqtSlot(str)
    def changestatusofalarm(self,status:str):
        if status == "LL ALARM":
            self.pvradiolowlowvalue.setChecked(True)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("ON")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
        if status == "HH ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(True)
            self.pvradiolowvalue.setChecked(False)
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("ON")
            self.pvradiohighvalue.setText("OFF")
        if status == "H ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(True)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("ON")
        if status == "L ALARM":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(True)
            self.pvradiolowvalue.setText("ON")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
        if status == "NORMAL":
            self.pvradiolowlowvalue.setChecked(False)
            self.pvradiohighvalue.setChecked(False)
            self.pvradiohighhighvalue.setChecked(False)
            self.pvradiolowvalue.setChecked(False)
            self.pvradiolowvalue.setText("OFF")
            self.pvradiolowlowvalue.setText("OFF")
            self.pvradiohighhighvalue.setText("OFF")
            self.pvradiohighvalue.setText("OFF")
    
class Chart(QtWidgets.QWidget):
    def __init__(self,itype,variableid,store,ranges):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.itype = itype
        self.variableid = variableid
        self.store = store
        self.ranges = ranges
        self._InitUI()
        
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.runchart()
        
    def runchart(self):
            self.trend = Trend(self.variableid,self.itype,self.store,self.ranges)
            self.vlayout.addWidget(self.trend)
            self.setLayout(self.vlayout)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AlarmPanel()
    window.show()
    sys.exit(app.exec())