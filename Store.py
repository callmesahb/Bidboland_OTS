from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot,QTimer,QMetaObject,QRunnable,QThreadPool
from OpcClient import OpcClient as opc
from workerThread import Worker
from StoreThread import StoreThread
import pandas as pd
import os
import sys
import json


class Store(QObject):
    updatevalues = pyqtSignal()
    def __init__(self,data,tags):
        super().__init__()
        self.tags = tags
        self.data = data
        current_path = os.getcwd()
        opc_path = os.path.join(current_path,"new opc")
        tags_path = os.path.join(current_path,"data")
        self.tagsfile = os.path.join(tags_path,"tags.json")
        self.certfile = os.path.join(opc_path,"cert.json")
        self.csvpath = os.path.join(opc_path,"tags.csv")
        self.csvfile = pd.read_csv(self.csvpath)
        self.opcSettings = self.read_json_file(self.certfile)
        url = self.opcSettings["endPointUrl"]
        self.opc = opc(url)
        self.datas = []
        for i in self.csvfile["tag"]:
            self.datas.append(i)
        # print(self.datas)
        self.newtags = {i: self.opc.getValue(i) for i in self.datas}

        
        self.finaltag = self.newtags
        self.getting_names()
        self.variables = self.getting_names()
        self.gettingvalvedata()
        self.tag = self.ReadingtagsFile()
        
        # self.worker.data_ready.connect(self.update_data)
        # self.worker.start()
        # self.ReadingTagClient()
        self.timer = QTimer(self)
        self.worker = StoreThread(self.opc,self.csvfile,self.tag)
        self.worker.start()
        self.timer.timeout.connect(self.ReadingTagClient)
        self.timer.start(1000)
    
    def update_data(self,newtags):
        self.updatevalues.emit(newtags,self.tag)
    def ReadingtagsFile(self) -> list:
        with open(self.tagsfile,"r") as file:
            data = json.load(file)
        return data
    
    def getting_names(self) -> list:
        self.names = []
        for i in self.tags:
            self.names.append(i["name"])
        return self.names
    
    def gettingvalvedata(self) -> dict:
        valves = []
        for i in self.tags:
            if "defaultValue" in i:
                valves.append(i)
        self.valve_value_map = {item['name']: item['initial'] for item in valves}
        return self.valve_value_map
    def setting_valueEV(self,varid):
        return self.valve_value_map.get(varid)
    
    def SettingInitial(self,varid) -> float:
        initial = 0.0
        if varid in self.names:
            varid_dict = next(item for item in self.tags if item['name'] == varid)
            initial = varid_dict["initial"]
        return round(initial,2)
    
    def SettingDetailsofsensor(self,varid:str) -> list:
        min = 0.0
        max = 0.0
        LL = 0.0
        HH = 0.0
        L = 0.0
        H = 0.0
        details = []
        if varid in self.names:
            varid_dict = next(item for item in self.tags if item['name'] == varid)
            min = varid_dict["R"][0]
            max = varid_dict["R"][1]
            LL = varid_dict["HHR"][0]
            HH = varid_dict["HHR"][1]
            L = varid_dict["HR"][0]
            H = varid_dict["HR"][1]
            details.append(min)
            details.append(max)
            details.append(LL)
            details.append(HH)
            details.append(L)
            details.append(H)
        return details
    def GettingUnit(self,varid) -> str:
        unit = ""
        if varid in self.names:
            varid_dict = next(item for item in self.tags if item['name'] == varid)
            unit = varid_dict["unit"]
        return unit

    def GettingControllerDetails(self,varid:str) -> list:
        Varid = varid.replace("OP","")
        sp = Varid + "SP"
        pv = Varid + "PV"
        op = Varid + "OP"
        tv = Varid + "TV"
        spvalue = 0.0
        pvvalue = 0.0
        opvalue = 0.0
        tvvalue = 1.0
        if sp in self.names or pv in self.names or op in self.names:
            varid_dict = next(item for item in self.tags if item['name'] == sp)
            varid_dict1 = next(item for item in self.tags if item['name'] == pv)
            varid_dict2 = next(item for item in self.tags if item['name'] == op)
            varid_dict3 = next(item for item in self.tags if item['name'] == tv)
            spvalue = varid_dict["initial"]
            pvvalue = varid_dict1["initial"]
            opvalue = varid_dict2["initial"]
            tvvalue = varid_dict3["initial"]
        oplist = [spvalue,pvvalue,opvalue , tvvalue]
        return oplist
    
    def ListingDescs(self,index:int) -> dict:
        page = self.data["layout"]["sections"][index]
        return page
    
    def GettingrangesofController(self,varid:str):
        varId = varid + "PV"
        if varId in self.names:
            varid_dict = next(item for item in self.tags if item['name'] == varId)
        

    def reset_to_initial(self):
        for item in self.tags:
            print(item)
            tag_name = item["name"]
            try:
                initial_value = item["initial"]
            except:
                initial_value = item["value"]
            self.finaltag[tag_name] = initial_value
            self.opc.setValue(tag_name,initial_value)
        self.updatevalues.emit()
    def read_json_file(self,file_path) -> dict:
        with open(file_path,"r") as file:
            data = json.load(file)
        return data

    def ReadingTagClient(self):
        self.finaltag=self.worker.finaltag
        self.updatevalues.emit()
        
    def settingValueOPC(self,varid,value):
        self.opc.setValue(varid,value)
        # pass
    
    # # def fetch_data(self):
    # #     newtags = {i: self.opc.getValue(i) for i in self.csvfile["tag"]}
    # #     if newtags != self.previous_tags:
    # #         self.previous_tags = newtags
    # #         self.updatevalues.emit(newtags, self.tags)
    
    # @pyqtSlot(dict,list)
    # def updating(self,data,tags):
    #     self.updatevalues.emit(data,tags)
