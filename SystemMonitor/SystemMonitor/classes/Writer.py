#!/usr/bin/python
# Wrote by: Aaron Baker
import csv
import os
import datetime
import platform
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU
import colorama 
from colorama import Fore, Back, Style

class Writer:
    def __init__(self, dir, subfolder, data, filename):
        self.dir = dir
        self.data = data if data != None else [] # will this need to hold dicts like {timestap : obj} if so use self.data[0].keys()[0] to get the then determin the class type
        self.filename = subfolder + "-" + filename + ".csv"
        self.fullpath = self.dir + self.filename
        if(platform.system() != "Windows"):
            self.fullpath = self.fullpath.replace("\\", "/")

        self.hasHeader = False
        return

    def Save_Averages(self):
        header = []
        if self.data.Get_Type() is Disks:
            print(Fore.GREEN + "   [-] Saving in writer for disk" + Style.RESET_ALL)
            headers = ["Disk Count", "Read Bytes", "Read Time", "Write Count", "Write Bytes", "Write Time"]
        elif self.data.Get_Type() is Memory:
            print(Fore.GREEN + "   [-] Saving in writer for memory" + Style.RESET_ALL)
            headers = ["VTotal", "VPercent Used", "VAvailable", "VUsed", "VFree", "STotal", "SPercent Used", "SUsed", "SFree", "SIN", "SOUT"]
        elif self.data.Get_Type() is Network:
            print(Fore.GREEN + "   [-] Saving in writer for network" + Style.RESET_ALL)
            headers = ["Bytes Sent", "Bytes Received", "Packets Sent", "Packets Received"]
        elif self.data.Get_Type() is CPU:
            print(Fore.GREEN + "   [-] Saving in writer for CPU" + Style.RESET_ALL)
            headers = ["User", "System", "Idle", "Interrupt", "DPC"]
        
        try:
            with open(self.fullpath, "w+", newline='') as file:
                filewriter = csv.writer(file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(headers)
                filewriter.writerow(self.data.Save_Averages())
        except Excetion as e:
            print("Error saving averages")
            print(e)
        return
    
    def Save_Info(self):
        headers = []
        rows = []
        classType = None
        cpuCount = 0
        if len(self.data) != 0:
            if type(self.data[0][list(self.data[0].keys())[0]]) is CPU:
                cpuCount = self.data[0][list(self.data[0].keys())[0]].Get_Core_Count()
                headers = ["Time", "User", "System", "Idle", "Interrupt", "DPC"]
                classType = CPU
            elif type(self.data[0][list(self.data[0].keys())[0]]) is Network:
                headers = ["Time", "Bytes Sent", "Bytes Received", "Packets Sent", "Packets Received"]
                classType = Network
            elif type(self.data[0][list(self.data[0].keys())[0]]) is Disks:
                headers = ["Time", "Disk Count", "Read Bytes", "Read Time", "Write Count", "Write Bytes", "Write Time"]
                classType = Disks
            elif type(self.data[0][list(self.data[0].keys())[0]]) is Memory:
                headers = ["Time", "VTotal", "VPercent Used", "VAvailable", "VUsed", "VFree", "STotal", "SPercent Used", "SUsed", "SFree", "SIN", "SOUT"]
                classType = Memory
            try:
                if classType != CPU:
                    with open(self.fullpath, "a+", newline='') as file:
                        filewriter = csv.writer(file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        if self.hasHeader is False:
                            filewriter.writerow(headers)
                            self.hasHeader = True
                        for d in self.data:
                            for k, v in d.items():
                                v.__class__ = classType # Changes the class to the needed class
                                toWrite = v.To_CSV_Array()
                                toWrite.insert(0, k)
                                filewriter.writerow(toWrite)
                    
                else:
                    for d in self.data:
                        for key, v in d.items():
                            ary = v.To_CSV_Array()
                            for k, v in ary.items():
                                filePath = self.fullpath.replace("CPU-", "CPU-" + str(k) + "-")
                                self.hasHeader = os.path.isfile(filePath)
                                with open(filePath, "a+", newline='') as file:
                                    filewriter = csv.writer(file, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    if self.hasHeader is False:
                                        filewriter.writerow(headers)
                                    v.insert(0, key)
                                    filewriter.writerow(v)

            except Exception as ex:
                print(ex)
        return

    def Update_Data(self, data):
        self.data.append(data)
        return

    def Clear_Date(self):
        self.data = []
        return