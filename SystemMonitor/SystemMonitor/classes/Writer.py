#!/usr/bin/python
# Wrote by: Aaron Baker
# This will need to be built using the factory patteren!
import csv
import os
import datetime
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU

class Writer:
    def __init__(self, dir, subfolder, data, date):
        self.dir = dir
        self.data = data if data != None else [] # will this need to hold dicts like {timestap : obj} if so use self.data[0].keys()[0] to get the then determin the class type
        self.filename = subfolder + "-" + date + ".csv"
        self.fullpath = self.dir + self.filename
        self.hasHeader = False
        return
    
    def Save_Info(self):
        headers = []
        rows = []
        classType = None
        cpuCount = 0
        if len(self.data) != 0:
            if type(self.data[0][list(self.data[0].keys())[0]]) is CPU:
                print("CPU TYPE : Finish writing for all CPUs")
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
                                print("Key " + k)
                                v.__class__ = classType # Changes the class to the needed class
                                toWrite = v.To_CSV_Array()
                                toWrite.insert(0, k)
                                filewriter.writerow(toWrite)
                    
                else:
                    print("Save for CPU Only")
                    #with open(self.fullpath.replace("CPU-", "CPU-" + str(count) + "-"), "a+") as file:
                    print("Cpu Count" + str(cpuCount))
                    
                    for d in self.data:
                        print("data")
                        print(d)
                        for key, v in d.items():
                            print("Key: " + key)
                            ary = v.To_CSV_Array()
                            for k, v in ary.items():
                                print(k)
                                print(v)
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