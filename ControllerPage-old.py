from PyQt6 import QtWidgets, QtCore,QtGui
from Store import Store
from Trend import Trend
from ControllerPagePlate import ControllerPlate
import sys

class ControllerPage(QtWidgets.QWidget):
    def __init__(self,itype:str,variableid:str,store:Store,name,pvvalues,varid,ranges,title):
        super().__init__()
        self.itype = itype
        self.variableid = variableid
        self.setWindowTitle(self.variableid)
        self.store = store
        self.name = name
        self.pvvalues = pvvalues
        self.varid = varid
        self.title = title
        self.ranges = ranges
        self.contplate = ControllerPlate(name,pvvalues,varid,store,ranges,itype,title)
        self.init_ui()
        
    def init_ui(self):
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.addWidget(self.contplate)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(MainTab(self.store,self.variableid),"Main")
        self.tabs.addTab(LoopTune(self.itype,self.variableid,self.store),"Loop Tune")
        self.tabs.addTab(SetPoint(self.variableid,self.store),"Set Point")
        self.tabs.addTab(PVandOP(self.store,self.variableid),"PV and OP")
        self.tabs.addTab(Alarms(self.variableid,self.store,self.name,self.pvvalues,self.ranges,self.itype,self.title),"Alarms")
        self.tabs.addTab(Connections(),"Connections")
        self.tabs.addTab(Chart(self.itype,self.variableid,self.store),"Chart")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.hlayout.addLayout(main_layout)
        self.setLayout(self.hlayout)
        # self.setWindowTitleجت با ۷ تب")
        
class MainTab(QtWidgets.QWidget):
    def __init__(self,store:Store,variableid):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.store = store
        self.variableid = variableid
        self.fontt.setBold(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getvalue)
        self.timer.start(1000)
        
        self.InitUI()
    def InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.vlayout2 = QtWidgets.QVBoxLayout()
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
        self.controlwindup()
        # self.setLayout(self.vlayout1)
        
    def controlwindup(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Control windup")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        g2layout.addWidget(QtWidgets.QLabel("Input windup status:"),1,0)
        g2layout.addWidget(QtWidgets.QLabel("Output windup status:"),2,0)
        windupstatus = QtWidgets.QLabel("No Windup(NORMAL)")
        windupstatus.setFont(self.fontt)
        g2layout.addWidget(windupstatus,2,1)
        self.vlayout1.addLayout(g2layout)
        # self.setLayout(self.vlayout1)
        self.controlwindup()
        
    def controlwindup(self):
        g3layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Safety interlock,Red tag and Operator tag")
        title.setFont(self.fontt)
        g3layout.addWidget(title,0,0)
        g3layout.addWidget(QtWidgets.QLabel("Safety interlock:"),1,0)
        off = QtWidgets.QRadioButton("OFF")
        off.setEnabled(False)
        g3layout.addWidget(off,1,1)
        g3layout.addWidget(QtWidgets.QLabel("Safety interlock option:"),2,0)
        interlockoptioncombo = QtWidgets.QComboBox()
        interlockoptioncombo.setFixedSize(100,25)
        interlockoptioncombo.setEnabled(False)
        interlockoptioncombo.setStyleSheet("color:gray")
        interlockoptioncombo.addItem("SHEDSAFE")
        badcontrolcombo = QtWidgets.QComboBox()
        badcontrolcombo.setStyleSheet("color:gray")
        badcontrolcombo.setEnabled(False)
        badcontrolcombo.addItem("SHEDHOLD")
        badcontrolcombo.setFixedSize(100,25)
        g3layout.addWidget(interlockoptioncombo,2,1)
        red = QtWidgets.QCheckBox("Red Tag")
        operator = QtWidgets.QCheckBox("Operator Tag")
        operator.setStyleSheet("color:gray;")
        operator.setEnabled(False)
        red.setEnabled(False)
        operator.setEnabled(False)
        g3layout.addWidget(red,3,0)
        g3layout.addWidget(operator,4,0)
        g3layout.addWidget(QtWidgets.QLabel("    Operator tag description:"),5,0)
        descoperator = QtWidgets.QLineEdit("Operator Tag")
        descoperator.setEnabled(False)
        descoperator.setFixedSize(100,25)
        descoperator.setReadOnly(True)
        g3layout.addWidget(descoperator,5,1)
        g3layout.addWidget(QtWidgets.QLabel("Bad control option:"),6,0)
        g3layout.addWidget(badcontrolcombo,6,1)
        g3layout.addWidget(QtWidgets.QLabel("Bad output connection option:"),7,0)
        badoutputoption = QtWidgets.QLineEdit("0.00")
        badoutputoption.setEnabled(False)
        badoutputoption.setFixedSize(100,25)
        badoutputoption.setReadOnly(True)
        g3layout.addWidget(badoutputoption,7,1)
        self.vlayout1.addLayout(g3layout)
        self.assignedcontroller()
        # self.setLayout(self.vlayout1)
    def assignedcontroller(self):
        g4layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Assigned controller")
        title.setFont(self.fontt)
        g4layout.addWidget(title,0,0)
        g4layout.addWidget(QtWidgets.QLabel("Controller name:"),1,0)
        g4layout.addWidget(QtWidgets.QLabel("Execution environment:"),2,0)
        self.vlayout1.addLayout(g4layout)
        self.alarmenableandsummary()
        # self.setLayout(self.vlayout1)
    def alarmenableandsummary(self):
        g5layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Alarm enable and summary")
        title.setFont(self.fontt)
        g5layout.addWidget(title,0,0)
        enblingalarm = QtWidgets.QCheckBox("Enabling Alarm")
        journal = QtWidgets.QCheckBox("Journal only option")
        journal.setEnabled(False)
        controlmodulecheck = QtWidgets.QCheckBox("OFF")
        controlmodulecheck.setChecked(False)
        controlmodulecheck.setCheckable(False)
        enblingalarm.setEnabled(False)
        g5layout.addWidget(enblingalarm,1,0)
        g5layout.addWidget(journal,2,0)
        g5layout.addWidget(QtWidgets.QLabel("Control module in alarm:"),3,0)
        g5layout.addWidget(QtWidgets.QLabel("OP high:"),3,2)
        g5layout.addWidget(QtWidgets.QLabel("OP low:"),4,2)
        g5layout.addWidget(QtWidgets.QLabel("Devation high:"),5,2)
        g5layout.addWidget(QtWidgets.QLabel("Devation low:"),6,2)
        g5layout.addWidget(QtWidgets.QLabel("Advisory devation:"),7,2)
        g5layout.addWidget(QtWidgets.QLabel("PV high-high:"),4,0)
        g5layout.addWidget(QtWidgets.QLabel("PV high:"),5,0)
        g5layout.addWidget(QtWidgets.QLabel("PV low:"),6,0)
        g5layout.addWidget(QtWidgets.QLabel("PV low-low:"),7,0)
        g5layout.addWidget(QtWidgets.QLabel("Positive rate of change:"),8,0)
        g5layout.addWidget(QtWidgets.QLabel("Negative rate of change:"),9,0)
        g5layout.addWidget(QtWidgets.QLabel("Bad PV:"),10,0)
        g5layout.addWidget(QtWidgets.QLabel("Safety interlock:"),8,2)
        g5layout.addWidget(QtWidgets.QLabel("Bad control:"),9,2)
        g5layout.addWidget(QtWidgets.QLabel("Uncommanded mode\nchange:"),10,2)
        # g5layout.addWidget(controlmodulecheck,3,1)
        # g5layout.addWidget(controlmodulecheck,4,1)
        # g5layout.addWidget(controlmodulecheck,5,1)
        # g5layout.addWidget(controlmodulecheck,6,1)
        # g5layout.addWidget(controlmodulecheck,7,1)
        for row in [3, 4, 5, 6, 7, 8, 9, 10]:
            ofcheck = QtWidgets.QCheckBox("OFF")
            ofcheck.setEnabled(False)
            ofcheck2 = QtWidgets.QCheckBox("OFF")
            ofcheck2.setEnabled(False)
            g5layout.addWidget(ofcheck, row, 1)
            g5layout.addWidget(ofcheck2, row, 3)
        
        # self.vlayout1.addLayout(g6layout)
        self.vlayout2.addLayout(g5layout)
        self.Mode()
        # self.setLayout(self.vlayout1)
    def Mode(self):
        g6layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Mode")
        title.setFont(self.fontt)
        g6layout.addWidget(title,0,0)
        g6layout.addWidget(QtWidgets.QLabel("Normal mode:"),1,0)
        g6layout.addWidget(QtWidgets.QLabel("Normal mode attribute:"),2,0)
        g6layout.addWidget(QtWidgets.QLabel("Permit operator mode changes:"),3,0)
        g6layout.addWidget(QtWidgets.QLabel("Permit external mode changes:"),4,0)
        g6layout.addWidget(QtWidgets.QLabel("Enable external mode changes:"),5,0)
        mode = QtWidgets.QComboBox()
        mode.setFixedSize(100,25)
        mode.addItem("AUTO")
        mode.setEnabled(False)
        g6layout.addWidget(mode,1,1)
        mode1 = QtWidgets.QComboBox()
        mode1.setFixedSize(100,25)
        mode1.addItem("OPERATOR")
        mode1.setEnabled(False)
        g6layout.addWidget(mode1,2,1)
        mode2 = QtWidgets.QComboBox()
        mode2.setFixedSize(100,25)
        mode2.addItem("PERMIT")
        mode2.setEnabled(False)
        g6layout.addWidget(mode2,3,1)
        mode3 = QtWidgets.QComboBox()
        mode3.addItem("PERMIT")
        mode3.setFixedSize(100,25)
        mode3.setEnabled(False)
        g6layout.addWidget(mode3,4,1)
        mode4 = QtWidgets.QComboBox()
        mode4.addItem("ENABLE")
        mode4.setEnabled(False)
        mode4.setFixedSize(100,25)
        g6layout.addWidget(mode4,5,1)
        self.vlayout2.addLayout(g6layout)
        # self.setLayout(self.vlayout2)
        self.modeattribute()
    def modeattribute(self):
        g7layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Mode")
        title.setFont(self.fontt)
        g7layout.addWidget(title,0,0)
        self.mancheck = QtWidgets.QCheckBox("MAN")
        self.mancheck.setEnabled(False)
        self.mancheck.setChecked(True)
        self.autocheck = QtWidgets.QCheckBox("AUTO")
        self.autocheck.setEnabled(False)
        self.autocheck.setChecked(True)
        self.cascheck = QtWidgets.QCheckBox("CAS")
        self.cascheck.setEnabled(False)
        program = QtWidgets.QCheckBox("PROGRAM")
        program.setEnabled(False)
        attr = QtWidgets.QCheckBox("Force mode attribute")
        attr.setEnabled(False)
        g7layout.addWidget(self.mancheck,1,0)
        g7layout.addWidget(self.autocheck,1,1)
        g7layout.addWidget(self.cascheck,1,2)
        g7layout.addWidget(program,1,3)
        g7layout.addWidget(attr,2,0)
        self.vlayout2.addLayout(g7layout)
        # self.setLayout(self.vlayout2)
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
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.setStretch(0,1)
        self.hlayout.setStretch(1,1)
        self.setLayout(self.hlayout)
        
    def getvalue(self):
        tvvarid = self.variableid + "TV"
        casvarid = self.variableid + "CAS"
        value = self.store.finaltag[tvvarid]
        value1 = self.store.finaltag[casvarid]
        if value1 == 1:
            self.mancheck.setChecked(False)
            self.autocheck.setChecked(False)
            self.cascheck.setChecked(True)
        
        
        
class SetPoint(QtWidgets.QWidget):
    def __init__(self,variableid,store):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.variable = variableid
        self.store = store
        values = self.store.spadfinder(variableid)
        self.spValue = self.store.spfinder(variableid)
        self.spadvalue = values
        self._InitUI()
    def _InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.vlayout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vlayout2 = QtWidgets.QVBoxLayout()
        self.vlayout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.SPtracking()
        
    def SPtracking(self):
        g1layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("SP processing/tracking")
        title.setFont(self.fontt)
        g1layout.addWidget(title,0,0)
        self.enablingspprocessing = QtWidgets.QCheckBox("Enable advisory SP processing")
        g1layout.addWidget(self.enablingspprocessing,1,0)
        self.enablingspprocessing.stateChanged.connect(self.putspadinopc)
        g1layout.addWidget(QtWidgets.QLabel("Advisory SP value:"),2,0)
        self.spvalue = QtWidgets.QLineEdit()
        self.spvalue.setPlaceholderText(str(self.spadvalue))
        self.spvalue.setReadOnly(False)
        self.spvalue.setEnabled(False)
        g1layout.addWidget(self.spvalue,2,1)
        enablepvtracking = QtWidgets.QCheckBox("Enable PV tracking")
        enablepvtracking2 = QtWidgets.QCheckBox("Enable PV tracking in auto/init")
        enablepvtracking.setChecked(True)
        enablepvtracking.setEnabled(False)
        enablepvtracking2.setEnabled(False)
        g1layout.addWidget(enablepvtracking,3,0)
        g1layout.addWidget(enablepvtracking2,4,0)
        g1layout.addWidget(QtWidgets.QLabel("Enable pushing SP:"),5,0)
        onoffpushingsp = QtWidgets.QRadioButton("OFF")
        onoffpushingsp.setEnabled(False)
        g1layout.addWidget(onoffpushingsp,5,1)
        self.vlayout1.addLayout(g1layout)
        # self.setLayout(self.vlayout1)
        self.SPRamping()
    def putspadinopc(self):
        sp = self.variable + "SP"
        if self.enablingspprocessing.isChecked():
            self.store.settingValueOPC(sp, self.spadvalue)
            self.spvalue.setReadOnly(True)
            self.spvalue.setEnabled(True)
        else:
            self.store.settingValueOPC(sp, self.spValue)
            print(self.store.settingValueOPC(sp, self.spValue))
            self.spvalue.setReadOnly(False)
            self.spvalue.setEnabled(False)

    def SPRamping(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Setpoint ramping")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        enablespramp = QtWidgets.QCheckBox("Set point ramping enabled")
        enablespramp.setEnabled(False)
        g2layout.addWidget(enablespramp,1,0)
        g2layout.addWidget(QtWidgets.QLabel("Set point ramping state:"),2,0)
        sprampingcombo = QtWidgets.QComboBox()
        sprampingcombo.addItem("OFF")
        sprampingcombo.setEnabled(False)
        g2layout.addWidget(sprampingcombo,2,1)
        g2layout.addWidget(QtWidgets.QLabel("Set point target value(SPTV):"),3,0)
        sptv = QtWidgets.QLineEdit("NaN")
        sptv.setEnabled(False)
        g2layout.addWidget(sptv,3,1)
        sppvtv = QtWidgets.QLineEdit("NaN")
        sppvtv.setEnabled(False)
        g2layout.addWidget(sppvtv,4,1)
        sppvtv = QtWidgets.QLineEdit("0.00")
        sppvtv.setEnabled(False)
        g2layout.addWidget(sppvtv,5,1)
        rampradio = QtWidgets.QRadioButton("OFF")
        rampradio.setChecked(True)
        rampradio.setEnabled(False)
        g2layout.addWidget(rampradio,6,1)
        reqramp = QtWidgets.QLineEdit("NaN")
        reqramp.setEnabled(False)
        g2layout.addWidget(reqramp,7,1)
        g2layout.addWidget(QtWidgets.QLabel("Maximum SP-PV deviation:"),4,0)
        g2layout.addWidget(QtWidgets.QLabel("SP tolerance:"),5,0)
        g2layout.addWidget(QtWidgets.QLabel("Ramp hold due to deviation:"),6,0)
        g2layout.addWidget(QtWidgets.QLabel("Requested ramp rate(EU/min):"),7,0)
        label = QtWidgets.QLabel("NaN")
        label.setStyleSheet("color:gray")
        g2layout.addWidget(label,8,1)
        g2layout.addWidget(QtWidgets.QLabel("Actual ramp rate(EU/min):"),8,0)
        g2layout.addWidget(QtWidgets.QLabel("Ramp time remaining(minutes):"),9,0)
        ramptime = QtWidgets.QLineEdit("0.00")
        ramptime.setEnabled(False)
        g2layout.addWidget(ramptime,9,1)
        pausesp = QtWidgets.QCheckBox("Pause SP ramping on anti-reset windup")
        pausesp.setChecked(True)
        pausesp.setEnabled(False)
        g2layout.addWidget(pausesp,10,0)
        self.vlayout1.addLayout(g2layout)
        self.sprange()
        # self.setLayout(self.vlayout1)
    def sprange(self):
        g3layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Set point input range(EU)")
        varid = self.variable
        title.setFont(self.fontt)
        g3layout.addWidget(title,0,0)
        g3layout.addWidget(QtWidgets.QLabel("High limit:"),1,0)
        tag = self.variable + "PV"
        highpvvalue = self.store.SettingDetailsofsensor(tag)[1]
        lowpvvalue = self.store.SettingDetailsofsensor(tag)[0]
        highvalue = QtWidgets.QLineEdit()
        highvalue.setText(str(highpvvalue))
        highvalue.setEnabled(False)
        g3layout.addWidget(highvalue,1,1)
        lowvalue = QtWidgets.QLineEdit()
        lowvalue.setEnabled(False)
        lowvalue.setText(str(lowpvvalue))
        g3layout.addWidget(lowvalue,2,1)
        g3layout.addWidget(QtWidgets.QLabel("low limit:"),2,0)
        self.vlayout2.addLayout(g3layout)
        self.Timeout()
        # self.setLayout(self.vlayout2)
    def Timeout(self):
        g4layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Timeout")
        title.setFont(self.fontt)
        g4layout.addWidget(title,0,0)
        g4layout.addWidget(QtWidgets.QLabel("Mode:"),1,0)
        modecombo = QtWidgets.QComboBox()
        modecombo.addItem("MAN")
        modecombo.setEnabled(False)
        g4layout.addWidget(modecombo,1,1)
        g4layout.addWidget(QtWidgets.QLabel("Time(seconds):"),2,0)
        timeline = QtWidgets.QLineEdit("0")
        timeline.setEnabled(False)
        g4layout.addWidget(timeline,2,1)
        self.vlayout2.addLayout(g4layout)
        self.hlayout.addLayout(self.vlayout1,0)
        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.setStretch(0,1)
        self.hlayout.setStretch(1,1)
        self.setLayout(self.hlayout)

class PVandOP(QtWidgets.QWidget):
    def __init__(self,store:Store,varid:str):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.store = store
        self.variableid = varid
        self._InitUI()
    def _InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.vlayout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vlayout2 = QtWidgets.QVBoxLayout()
        self.vlayout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.ProcessVariable()
    
    def ProcessVariable(self):
        g1layout = QtWidgets.QGridLayout()
        font = QtGui.QFont("Arial")
        font.setBold(True)
        title = QtWidgets.QLabel("Process variable")
        title.setFont(self.fontt)
        g1layout.addWidget(title,0,0)
        g1layout.addWidget(QtWidgets.QLabel("PV high range (EU):PIDA"),1,0)
        varid = self.variableid + "PV"
        highvalue = self.store.SettingDetailsofsensor(varid)[1]
        lowvalue = self.store.SettingDetailsofsensor(varid)[0]
        pvhighrange = QtWidgets.QLabel(str(highvalue))
        pvhighrange.setFont(font)
        pvlowrange = QtWidgets.QLabel(str(lowvalue))
        pvlowrange.setFont(font)
        g1layout.addWidget(pvhighrange,1,1)
        g1layout.addWidget(pvlowrange,2,1)
        g1layout.addWidget(QtWidgets.QLabel("PV low range (EU):PIDA"),2,0)
        g1layout.addWidget(QtWidgets.QLabel("PV characterization:DACA"),3,0)
        g1layout.addWidget(QtWidgets.QLabel("LINEAR"),3,1)
        g1layout.addWidget(QtWidgets.QLabel("PV status:DACA"),4,0)
        g1layout.addWidget(QtWidgets.QLabel("NORMAL"),4,1)
        g1layout.addWidget(QtWidgets.QLabel("PV source option:DACA"),5,0)
        pvsourceoption = QtWidgets.QComboBox()
        pvsourceoption.addItem("ALL")
        pvsourceoption.setEnabled(False)
        g1layout.addWidget(pvsourceoption,5,1)
        g1layout.addWidget(QtWidgets.QLabel("PV source:DACA"),6,0)
        pvsource = QtWidgets.QComboBox()
        pvsource.addItem("AUTO")
        pvsource.setEnabled(False)
        g1layout.addWidget(pvsource,6,1)
        g1layout.addWidget(QtWidgets.QLabel("Manual PV option:DACA"),7,0)
        manualpvoption = QtWidgets.QComboBox()
        manualpvoption.addItem("SHEDHOLD")
        manualpvoption.setEnabled(False)
        g1layout.addWidget(manualpvoption,7,1)
        g1layout.addWidget(QtWidgets.QLabel("Manual PV value:DACA"),8,0)
        
        manualpvvalue = QtWidgets.QLineEdit()
        manualpvvalue.setEnabled(False)
        g1layout.addWidget(manualpvvalue,8,1)
        g1layout.addWidget(QtWidgets.QLabel("PV high limit(EU):DACA"),9,0)
        pvhighlimitvalue = highvalue + 0.03*highvalue
        pvhighlimit = QtWidgets.QLabel(str(pvhighlimitvalue))
        pvhighlimit.setFont(font)
        g1layout.addWidget(pvhighlimit,9,1)
        pvhighrange = QtWidgets.QLabel(str(highvalue))
        pvhighrange.setFont(font)
        g1layout.addWidget(pvhighrange,10,1)
        g1layout.addWidget(QtWidgets.QLabel("PV high range(EU):DACA"),10,0)
        g1layout.addWidget(QtWidgets.QLabel("PV low range:DACA"),11,0)
        pvlowrangevalue = QtWidgets.QLabel(str(lowvalue))
        pvlowrangevalue.setFont(font)
        g1layout.addWidget(pvlowrangevalue,11,1)
        pvlowlimitvalue = lowvalue - 0.03 * lowvalue
        pvlowlimit = QtWidgets.QLabel(str(pvlowlimitvalue))
        pvlowlimit.setFont(font)
        g1layout.addWidget(pvlowlimit,12,1)
        g1layout.addWidget(QtWidgets.QLabel("PV low limit:DACA"),12,0)
        self.vlayout1.addLayout(g1layout)
        self.Clamping()
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
        line1 = QtWidgets.QLineEdit("0.02")
        line1.setFixedSize(200,25)
        line1.setEnabled(False)
        g2layout.addWidget(line1,2,1,QtCore.Qt.AlignmentFlag.AlignLeft)
        line2 = QtWidgets.QLineEdit("NaN")
        line2.setFixedSize(200,25)
        line2.setEnabled(False)
        g2layout.addWidget(line2,3,1)
        self.vlayout1.addLayout(g2layout)
        # self.setLayout(self.vlayout1)
        self.Output()
    def Output(self):
        g3layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Output")
        title.setFont(self.fontt)
        g3layout.addWidget(title,0,0)
        g3layout.addWidget(QtWidgets.QLabel("Extended high limit(%):"),1,0)
        extendedhl = QtWidgets.QLineEdit("106.9")
        extendedhl.setEnabled(False)
        g3layout.addWidget(extendedhl,1,1)
        g3layout.addWidget(QtWidgets.QLabel("high limit(%):"),2,0)
        hl = QtWidgets.QLineEdit("105.0")
        hl.setEnabled(False)
        g3layout.addWidget(hl,2,1)
        g3layout.addWidget(QtWidgets.QLabel("low limit(%):"),3,0)
        ll = QtWidgets.QLineEdit("5")
        ll.setEnabled(False)
        g3layout.addWidget(ll,3,1)
        g3layout.addWidget(QtWidgets.QLabel("Extended low limit(%):"),4,0)
        extendedll = QtWidgets.QLineEdit("-6.9")
        extendedll.setEnabled(False)
        g3layout.addWidget(extendedll,4,1)
        g3layout.addWidget(QtWidgets.QLabel("Rate of change limit(%)::"),5,0)
        rcl = QtWidgets.QLineEdit("NaN")
        rcl.setEnabled(False)
        g3layout.addWidget(rcl,5,1)
        g3layout.addWidget(QtWidgets.QLabel("Minimum change(%):"),6,0)
        mc = QtWidgets.QLineEdit("0.0")
        mc.setEnabled(False)
        g3layout.addWidget(mc,6,1)
        g3layout.addWidget(QtWidgets.QLabel("Safe output(%):"),7,0)
        safeoutput = QtWidgets.QLineEdit("10.0")
        safeoutput.setEnabled(False)
        g3layout.addWidget(safeoutput,7,1)
        g3layout.addWidget(QtWidgets.QLabel("OP tolerance(%):"),8,0)
        OPtole = QtWidgets.QLineEdit("0.0")
        OPtole.setEnabled(False)
        g3layout.addWidget(OPtole,8,1)
        g3layout.addWidget(QtWidgets.QLabel("Output indication:"),9,0)
        combo = QtWidgets.QComboBox()
        combo.addItem("Direct")
        combo.setEnabled(False)
        g3layout.addWidget(combo,9,1)
        self.vlayout2.addLayout(g3layout)
        # self.setLayout(self.vlayout2)
        self.Outputbias()
    def Outputbias(self):
        g4layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Output bias")
        title.setFont(self.fontt)
        g4layout.addWidget(title,0,0)
        g4layout.addWidget(QtWidgets.QLabel("Output bias:"),1,0)
        line1 = QtWidgets.QLineEdit("0.00")
        line1.setFixedSize(100,25)
        line1.setEnabled(False)
        g4layout.addWidget(line1,1,3)
        g4layout.addWidget(QtWidgets.QLabel("Fix:"),2,0)
        fixvalue = QtWidgets.QLineEdit("0.0")
        fixvalue.setFixedSize(100,25)
        fixvalue.setEnabled(False)
        g4layout.addWidget(fixvalue,2,1)
        g4layout.addWidget(QtWidgets.QLabel("Float:"),2,2)
        g4layout.addWidget(QtWidgets.QLabel("0.0"),2,3)
        g4layout.addWidget(QtWidgets.QLabel("Output bias rate:"),3,0)
        opbiasrate = QtWidgets.QLineEdit("NaN")
        opbiasrate.setFixedSize(100,25)
        opbiasrate.setEnabled(False)
        g4layout.addWidget(opbiasrate,3,1)
        self.vlayout2.addLayout(g4layout)
        # self.setLayout(self.vlayout2)
        self.ControlOptions()
    def ControlOptions(self):
        g5layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Control options")
        title.setFont(self.fontt)
        g5layout.addWidget(title,0,0)
        g5layout.addWidget(QtWidgets.QLabel("Secondary initialization option:"),1,0)
        line1 = QtWidgets.QComboBox()
        line1.addItem("DISABLE")
        line1.setEnabled(False)
        g5layout.addWidget(line1,1,1)
        g5layout.addWidget(QtWidgets.QLabel("Bad control option::"),2,0)
        line2 = QtWidgets.QComboBox()
        line2.addItem("SHEDHOLD")
        line2.setEnabled(False)
        g5layout.addWidget(line2,2,1)
        line1.setFixedSize(100,25)
        line2.setFixedSize(100,25)
        self.vlayout2.addLayout(g5layout)
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.setLayout(self.hlayout)
        
class Connections(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self._InitUI()
    def _InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.vlayout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vlayout2 = QtWidgets.QVBoxLayout()
        self.vlayout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.SCMconnection()
    def SCMconnection(self):
        g1layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("SCM connection")
        title.setFont(self.fontt)
        g1layout.addWidget(title,0,0)
        g1layout.addWidget(QtWidgets.QLabel("SCM option:"),1,0)
        scmoptionvalue = QtWidgets.QLabel("NONE")
        scmoptionvalue.setFont(self.fontt)
        g1layout.addWidget(scmoptionvalue,1,1)
        g1layout.addWidget(QtWidgets.QLabel("Moitored SCM name:"),2,0)
        g1layout.addWidget(QtWidgets.QLabel("SCM state:"),3,0)
        g1layout.addWidget(QtWidgets.QLabel("SCM mode:"),4,0)
        scmmodevalue = QtWidgets.QLabel("NONE")
        scmmodevalue.setFont(self.fontt)
        g1layout.addWidget(scmmodevalue,4,1)
        g1layout.addWidget(QtWidgets.QLabel("Mode tracking option:"),5,0)
        modetrcptionvalue = QtWidgets.QLabel("ONESHOT")
        modetrcptionvalue.setFont(self.fontt)
        g1layout.addWidget(modetrcptionvalue,5,1)
        g1layout.addWidget(QtWidgets.QLabel("Restart state option:"),6,0)
        restartstateoptionvalue = QtWidgets.QLabel("NONE")
        restartstateoptionvalue.setFont(self.fontt)
        g1layout.addWidget(restartstateoptionvalue,6,1)
        self.vlayout1.addLayout(g1layout)
        # self.setLayout(self.vlayout1)
        self.SCMstateoption()
    def SCMstateoption(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("SCM state option")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        stateoption = QtWidgets.QLabel("State option")
        stateoption.setFont(self.fontt)
        g2layout.addWidget(stateoption,1,0)
        starting = QtWidgets.QLabel("Starting")
        starting.setFont(self.fontt)
        g2layout.addWidget(starting,1,1)
        stop = QtWidgets.QLabel("Stop")
        stop.setFont(self.fontt)
        g2layout.addWidget(stop,1,2)
        holding = QtWidgets.QLabel("Holding")
        holding.setFont(self.fontt)
        g2layout.addWidget(holding,1,3)
        self.vlayout1.addLayout(g2layout)
        g2layout.addWidget(QtWidgets.QLabel("Type"),2,0)
        g2layout.addWidget(QtWidgets.QLabel("None"),2,1)
        g2layout.addWidget(QtWidgets.QLabel("None"),2,2)
        g2layout.addWidget(QtWidgets.QLabel("None"),2,3)
        g2layout.addWidget(QtWidgets.QLabel("Value"),3,0)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),3,1)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),3,2)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),3,3)
        g2layout.addWidget(QtWidgets.QLabel("Set point rate"),4,0)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),4,1)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),4,2)
        g2layout.addWidget(QtWidgets.QLabel("NaN"),4,3)
        # self.setLayout(self.vlayout1)
        self.dispinfo()
        
    def dispinfo(self):
        g3layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Display information")
        title.setFont(self.fontt)
        g3layout.addWidget(title,0,0)
        g3layout.addWidget(QtWidgets.QLabel("Point detail display:"),1,0)
        g3layout.addWidget(QtWidgets.QLabel("Group detail display:"),2,0)
        g3layout.addWidget(QtWidgets.QLabel("Associated display:"),3,0)
        self.vlayout2.addLayout(g3layout)
        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)
        self.setLayout(self.hlayout)
class Alarms(QtWidgets.QWidget):
    def __init__(self,variableid,store:Store,name,pvvalues,ranges,type,title):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.store = store
        self.variableid = variableid
        self.name = name
        self.pvvalues = pvvalues
        self.ranges = ranges
        self.type = type
        self.title = title
        self.contplate = ControllerPlate(name,pvvalues,variableid,store,ranges,type,title)
        self.contplate.updatestatus.connect(self.changestatusofalarm)
        self._initUI()
    def _initUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.Alarmconf()
    
    def Alarmconf(self):
        nonecut = [11,12,17]
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
        Enable = QtWidgets.QLabel("Enable")
        Enable.setFont(self.fontt)
        g1layout.addWidget(Enable,1,3)
        Trip_point = QtWidgets.QLabel("Trip point")
        Trip_point.setFont(self.fontt)
        g1layout.addWidget(Trip_point,1,4)
        Priority = QtWidgets.QLabel("Priority")
        Priority.setFont(self.fontt)
        g1layout.addWidget(Priority,1,5)
        Severity = QtWidgets.QLabel("Severity")
        Severity.setFont(self.fontt)
        g1layout.addWidget(Severity,1,6)
        Ondelaytime = QtWidgets.QLabel("On-Delay\ntime(Sec)")
        Ondelaytime.setFont(self.fontt)
        g1layout.addWidget(Ondelaytime,1,7)
        offdelaytime = QtWidgets.QLabel("Off-Delay\ntime(Sec)")
        offdelaytime.setFont(self.fontt)
        g1layout.addWidget(offdelaytime,1,8)
        deadboundvalue = QtWidgets.QLabel("Deadband\n  value")
        deadboundvalue.setFont(self.fontt)
        g1layout.addWidget(deadboundvalue,1,9)
        Deadbandunits = QtWidgets.QLabel("Deadband\n  units")
        Deadbandunits.setFont(self.fontt)
        g1layout.addWidget(Deadbandunits,1,10)
        g1layout.addWidget(QtWidgets.QLabel("PV high-high:"),2,0)
        g1layout.addWidget(QtWidgets.QLabel("PV high:"),3,0)
        g1layout.addWidget(QtWidgets.QLabel("PV low:"),4,0)
        g1layout.addWidget(QtWidgets.QLabel("PV low-low:"),5,0)
        g1layout.addWidget(QtWidgets.QLabel("Positive rate of change:"),6,0)
        g1layout.addWidget(QtWidgets.QLabel("Negative rate of change:"),7,0)
        g1layout.addWidget(QtWidgets.QLabel("Bad PV:"),8,0)
        g1layout.addWidget(QtWidgets.QLabel("OP high:"),9,0)
        g1layout.addWidget(QtWidgets.QLabel("OP low:"),10,0)
        g1layout.addWidget(QtWidgets.QLabel("Deviation high:"),11,0)
        g1layout.addWidget(QtWidgets.QLabel("Deviation low:"),12,0)
        g1layout.addWidget(QtWidgets.QLabel("Advisory deviation:"),13,0)
        g1layout.addWidget(QtWidgets.QLabel("Safety interlock:"),14,0)
        g1layout.addWidget(QtWidgets.QLabel("Bad control:"),15,0)
        g1layout.addWidget(QtWidgets.QLabel("Uncommanded mode change:"),16,0)
        g1layout.addWidget(QtWidgets.QLabel("Bad Output:"),17,0)
        pvradiohighhighvalue = QtWidgets.QRadioButton("OFF")
        pvradiohighhighvalue.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: gray;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
        pvradiohighhighvalue.setEnabled(False)
        pvradiohighhighvalue.setChecked(True)
        g1layout.addWidget(pvradiohighhighvalue,2,1)
        pvhighhighvalue = QtWidgets.QLineEdit("NaN")
        pvhighhighvalue.setEnabled(False)
        pvhighhighvalue.setFixedSize(80,25)
        g1layout.addWidget(pvhighhighvalue,4,4)
        varid = self.variableid + "PV"
        highvalue = self.store.SettingDetailsofsensor(varid)[5]
        lowvalue = self.store.SettingDetailsofsensor(varid)[4]
        pvhighvalue = QtWidgets.QLineEdit()
        pvhighvalue.setText(str(highvalue))
        pvhighvalue.setEnabled(False)
        pvhighvalue.setFixedSize(80,25)
        g1layout.addWidget(pvhighvalue,3,4)
        pvlowvalue = QtWidgets.QLineEdit()
        pvlowvalue.setText(str(lowvalue))
        pvlowvalue.setEnabled(False)
        pvlowvalue.setFixedSize(80,25)
        g1layout.addWidget(pvlowvalue,4,4)
        self.status = "OFF"
        self.pvradiohighvalue = QtWidgets.QRadioButton(self.status)
        self.pvradiohighvalue.setEnabled(False)
        g1layout.addWidget(self.pvradiohighvalue,3,1)
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

        self.pvlowradio = QtWidgets.QRadioButton("OFF")
        # self.pvlowradio.setCheckable(False)
        self.pvlowradio.setEnabled(False)
        self.pvlowradio.setStyleSheet("""
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
        g1layout.addWidget(self.pvlowradio,4,1)
        self.radiogroup = QtWidgets.QButtonGroup(self)
        self.radiogroup.setExclusive(False)
        self.radiogroup.addButton(self.pvradiohighvalue)
        self.radiogroup.addButton(self.pvlowradio)

        for i in range(2,18):
            line = QtWidgets.QLineEdit("0")
            line2 = QtWidgets.QLineEdit("0")
            line.setFixedSize(60,25)
            line2.setFixedSize(60,25)
            line.setEnabled(False)
            line2.setEnabled(False)
            line3 = QtWidgets.QLineEdit("0")
            line3.setFixedSize(60,25)
            line3.setEnabled(False)
            g1layout.addWidget(line,i,6)
            if i in [14,16,17]:
                continue
            g1layout.addWidget(line2,i,7)
            g1layout.addWidget(line3,i,8)
        for i in range(2,14):
            if i in [6,7,8]:
                continue
            line3 = QtWidgets.QLineEdit("2")
            line3.setFixedSize(60,25)
            line3.setEnabled(False)
            g1layout.addWidget(line3,i,9)
        for i in range(5,18):
            radio = QtWidgets.QRadioButton("OFF")
            radio.setStyleSheet("""
                QRadioButton::indicator {
                    background-color: red;
                    border: 1px solid gray;
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                }
                QRadioButton::indicator:checked {
                    background-color: gray;
                }
                QRadioButton::indicator:unchecked {
                    background-color: black;
                }
                """)
            radio.setEnabled(False)
            radio.setChecked(True)
            g1layout.addWidget(radio,i,1)
        for i in range(2,9):
            g1layout.addWidget(QtWidgets.QLabel("DACA"),i,2)
        for i in range(2,14):
            if i in [6,7,8]:
                continue
            radiobtn = QtWidgets.QRadioButton("EU")
            radiobtn.setChecked(True)
            radiobtn.setEnabled(False)
            g1layout.addWidget(radiobtn,i,10)
        for j in range(9,18):
            g1layout.addWidget(QtWidgets.QLabel("PIDA"),j,2)
        for i in range(5,14):
            if i == 8:
                continue
            l = QtWidgets.QLineEdit("NaN")
            l.setEnabled(False)
            g1layout.addWidget(l,i,4)
        for i in [2,5]:
            c = QtWidgets.QComboBox()
            c.addItem("HIGH")
            c.setEnabled(False)
            g1layout.addWidget(c,i,5)
        for i in [3,4,6,7,11,12]:
            c = QtWidgets.QComboBox()
            c.addItem("LOW")
            c.setEnabled(False)
            g1layout.addWidget(c,i,5)
        for i in range(9,18):
            if i in nonecut:
                continue
            else:
                c = QtWidgets.QComboBox()
                c.addItem("NONE")
                c.setEnabled(False)
                g1layout.addWidget(c,i,5)
        advisoryvalue = QtWidgets.QCheckBox()
        advisoryvalue.setEnabled(False)
        g1layout.addWidget(advisoryvalue,13,3)
        safetyinterlockvalue = QtWidgets.QCheckBox()
        safetyinterlockvalue.setEnabled(False)
        g1layout.addWidget(safetyinterlockvalue,14,3)
        uncommandedvalue = QtWidgets.QCheckBox()
        uncommandedvalue.setEnabled(False)
        g1layout.addWidget(uncommandedvalue,16,3)
        c = QtWidgets.QComboBox()
        c.addItem("URGENT")
        c.setEnabled(False)
        g1layout.addWidget(c,8,5)
        d = QtWidgets.QComboBox()
        d.addItem("URGENT")
        d.setEnabled(False)
        g1layout.addWidget(d,17,5)
        self.vlayout.addLayout(g1layout)
        self.DACAblockoption()
    
    @QtCore.pyqtSlot(str)
    def changestatusofalarm(self,status:str):
        if status == "LL ALARM":
            self.status = "ON"
            self.pvlowradio.setChecked(True)
            self.pvradiohighvalue.setChecked(False)
            self.pvlowradio.setText("ON")
            self.pvradiohighvalue.setText("OFF")
        if status == "HH ALARM":
            self.status = "ON"
            self.pvradiohighvalue.setChecked(True)
            self.pvlowradio.setChecked(False)
            self.pvradiohighvalue.setText("ON")
            self.pvlowradio.setText("OFF")
        if status == "NORMAL":
            self.status = "ON"
            self.pvradiohighvalue.setChecked(False)
            self.pvlowradio.setChecked(False)
            self.pvradiohighvalue.setText("OFF")
            self.pvlowradio.setText("OFF")
            
            
        # else:
        #     self.status = "OFF"
        #     self.pvradiohighvalue.setChecked(False)
        # self.setLayout(self.vlayout)
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
        
class LoopTune(QtWidgets.QWidget):
    def __init__(self,itype,variableid,store):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.itype = itype
        self.variableid = variableid
        self.store = store
        self.tivalue = 5
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getValues)
        self.timer.start(1000)
        self.ti = self.store.tifinder(variableid)
        self.gain = self.store.gainfinder(variableid)
        self._InitUI()
    def _InitUI(self):
        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.hlayout = QtWidgets.QHBoxLayout()
        self.runchart()
    def runchart(self):
        self.trend = Trend(self.variableid,self.itype,self.store)
        self.vlayout1.addWidget(self.trend)
        self.Tuninggeneral()
        
    def Tuninggeneral(self):
        g1layout = QtWidgets.QGridLayout()
        g1layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        title = QtWidgets.QLabel("Tuning - general")
        title.setFont(self.fontt)
        g1layout.addWidget(title,0,0)
        g1layout.addWidget(QtWidgets.QLabel("Control equation:"),1,0)
        g1layout.addWidget(QtWidgets.QLabel("Control action:"),2,0)
        g1layout.addWidget(QtWidgets.QLabel("Integral time T1 (minutes):"),3,0)
        g1layout.addWidget(QtWidgets.QLabel("Low limit:"),4,0)
        g1layout.addWidget(QtWidgets.QLabel("High limit:"),4,2)
        g1layout.addWidget(QtWidgets.QLabel("Derivative time T2 (miutes):"),5,0)
        g1layout.addWidget(QtWidgets.QLabel("Low limit:"),6,0)
        g1layout.addWidget(QtWidgets.QLabel("High limit:"),6,2)
        g1layout.addWidget(QtWidgets.QLabel("Filter time(miutes):"),7,0)
        controleqnvalue = QtWidgets.QComboBox()
        controleqnvalue.addItem("EQB")
        controleqnvalue.setEnabled(False)
        g1layout.addWidget(controleqnvalue,1,1)
        cntaction = QtWidgets.QComboBox()
        cntaction.addItem("DIRECT")
        cntaction.setEnabled(False)
        g1layout.addWidget(cntaction,2,1)
        self.integraltimevalue = QtWidgets.QLineEdit(str(self.ti))
        
        g1layout.addWidget(self.integraltimevalue,3,1)
        self.integraltimevalue.returnPressed.connect(self.on_integral_time_changed)
        lowlimitvalue1 = QtWidgets.QLineEdit("0.0")
        lowlimitvalue1.setEnabled(False)
        g1layout.addWidget(lowlimitvalue1,4,1)
        highlimitvalue1 = QtWidgets.QLineEdit("1000.0")
        highlimitvalue1.setEnabled(False)
        g1layout.addWidget(highlimitvalue1,4,3)
        integraltimevalue2 = QtWidgets.QLineEdit("0.0")
        integraltimevalue2.setEnabled(False)
        g1layout.addWidget(integraltimevalue2,5,1)
        lowlimitvalue2 = QtWidgets.QLineEdit("0.0")
        lowlimitvalue2.setEnabled(False)
        g1layout.addWidget(lowlimitvalue2,6,1)
        highlimitvalue2 = QtWidgets.QLineEdit("1000.0")
        highlimitvalue2.setEnabled(False)
        g1layout.addWidget(highlimitvalue2,6,3)
        filtertimevalue = QtWidgets.QLineEdit("0.2")
        filtertimevalue.setEnabled(False)
        g1layout.addWidget(filtertimevalue,7,1)
        self.hlayout.addLayout(g1layout)
        # self.setLayout(self.vlayout1)
        self.Gainoptions()
    def on_integral_time_changed(self):
        try:
            varid = self.variableid + "TI"
            new_ti = float(self.integraltimevalue.text())
            if new_ti != self.ti:
                self.ti = new_ti
                self.store.settingValueOPC(varid,new_ti)
                print(f"TI updated to {new_ti}")
        except ValueError:
            print("Invalid input for TI")
            
        # valueofti = self.store.finaltag[tivarid]
        # self.integraltimevalue.setText(str(valueofti))
    
    def Gainoptions(self):
        g2layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Gain options")
        title.setFont(self.fontt)
        g2layout.addWidget(title,0,0)
        g2layout.addWidget(QtWidgets.QLabel("Gain options:"),1,0)
        g2layout.addWidget(QtWidgets.QLabel("Overall gain:"),2,0)
        g2layout.addWidget(QtWidgets.QLabel("Low limit:"),3,0)
        g2layout.addWidget(QtWidgets.QLabel("High limit:"),3,2)
        g2layout.addWidget(QtWidgets.QLabel("Linear gain factor:"),4,0)
        g2layout.addWidget(QtWidgets.QLabel("Gap gain factor:"),5,0)
        g2layout.addWidget(QtWidgets.QLabel("Low limit:"),6,0)
        g2layout.addWidget(QtWidgets.QLabel("High limit:"),6,2)
        g2layout.addWidget(QtWidgets.QLabel("Non linearity form:"),7,0)
        g2layout.addWidget(QtWidgets.QLabel("Non linear gain factor:"),8,0)
        g2layout.addWidget(QtWidgets.QLabel("External gain factor:"),9,0)
        checkbox = QtWidgets.QCheckBox("Legacy gap")
        checkbox.setChecked(True)
        checkbox.setEnabled(False)
        g2layout.addWidget(checkbox,10,0)
        
        gainoptionvalue = QtWidgets.QComboBox()
        gainoptionvalue.addItem("LIN")
        gainoptionvalue.setEnabled(False)
        g2layout.addWidget(checkbox,1,1)
        
        self.overallgainoptionvalue = QtWidgets.QLineEdit(str(self.gain))
        self.overallgainoptionvalue.returnPressed.connect(self.on_gain_changed)
        g2layout.addWidget(self.overallgainoptionvalue,2,1)
        
        lowlimitvalu1 = QtWidgets.QLineEdit("0.0")
        lowlimitvalu1.setEnabled(False)
        g2layout.addWidget(lowlimitvalu1,3,1)
        
        highlimitvalu1 = QtWidgets.QLineEdit("100.0")
        highlimitvalu1.setEnabled(False)
        g2layout.addWidget(highlimitvalu1,3,3)
        
        lingainfactor = QtWidgets.QLineEdit("NaN")
        lingainfactor.setEnabled(False)
        g2layout.addWidget(lingainfactor,4,1)
        
        gpgainfc = QtWidgets.QLineEdit("0.0")
        gpgainfc.setEnabled(False)
        g2layout.addWidget(gpgainfc,5,1)
        
        lowlimitvalu2 = QtWidgets.QLineEdit("0.0")
        lowlimitvalu2.setEnabled(False)
        g2layout.addWidget(lowlimitvalu2,6,1)
        
        highlimitvalue2 = QtWidgets.QLineEdit("100.0")
        highlimitvalue2.setEnabled(False)
        g2layout.addWidget(highlimitvalue2,6,3)
        
        nonlntyform = QtWidgets.QLineEdit("0")
        nonlntyform.setEnabled(False)
        g2layout.addWidget(nonlntyform,7,1)
        
        nonlntygainform = QtWidgets.QLineEdit("0")
        nonlntygainform.setEnabled(False)
        g2layout.addWidget(nonlntygainform,8,1)
        
        nonlntyform = QtWidgets.QLineEdit("NaN")
        nonlntyform.setEnabled(False)
        g2layout.addWidget(nonlntyform,9,1)
        
        nonlntyform = QtWidgets.QLineEdit("NaN")
        nonlntyform.setEnabled(False)
        g2layout.addWidget(nonlntyform,10,1)
        
        self.hlayout.addLayout(g2layout)
        self.vlayout1.addLayout(self.hlayout)
        self.setLayout(self.vlayout1)
    def getValues(self):
        tivarid = self.variableid + "TI"
        kcvarid = self.variableid + "KC"
        if not self.integraltimevalue.hasFocus():
            valueofti = self.store.finaltag[tivarid]
            self.integraltimevalue.setText(str(valueofti))
        if not self.overallgainoptionvalue.hasFocus():
            valueofkc = self.store.finaltag[kcvarid]
            self.overallgainoptionvalue.setText(str(valueofkc))
            
    def on_gain_changed(self):
        try:
            varid = self.variableid + "KC"
            new_gain = float(self.overallgainoptionvalue.text())
            if new_gain != self.gain:
                self.gain = new_gain
                self.store.settingValueOPC(varid,new_gain)
                print(f"TI updated to {new_gain}")
        except ValueError:
            print("Invalid input for TI")


class Chart(QtWidgets.QWidget):
    def __init__(self,itype,variableid,store):
        super().__init__()
        self.fontt = QtGui.QFont("New Times Roman")
        self.fontt.setBold(True)
        self.itype = itype
        self.variableid = variableid
        self.store = store
        self._InitUI()
        
    def _InitUI(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.runchart()
        
    def runchart(self):
            self.trend = Trend(self.variableid,self.itype,self.store)
            self.vlayout.addWidget(self.trend)
            self.setLayout(self.vlayout)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ControllerPage()
    window.show()
    sys.exit(app.exec())