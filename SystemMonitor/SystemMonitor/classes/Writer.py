#!/usr/bin/python
# Wrote by: Aaron Baker
# This will need to be built using the factory patteren!
import csv
import datetime
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU

class Writer:
    dir = None
    fullpath = None
    filename = None
    data = None 
    time = None
    hasHeader = False
    
    def __init__(self, dir, subfolder, data):
        self.dir = dir
        self.data = data if data != None else []
        self.filename = subfolder + "-" + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + ".csv"
        self.fullpath = self.dir + self.filename
        return
    
    def Save_Info(self):
        headers = []
        rows = []
        if len(self.data) != 0:
            if type(self.data[0]) is CPU:
                print("CPU TYPE")
            elif type(self.data[0]) is Network:
                print("Network TYPE")
                headers = ["Bytes Sent", "Bytes Received", "Packets Sent", "Packets Received"]
            elif type(self.data[0]) is Disks:
                print("Disks TYPE")
                headers = ["Disk Count", "Read Bytes", "Read Time", "Write Count", "Write Bytes", "Write Time"]
            elif type(self.data[0]) is Memory:
                print("Memory TYPE")
                headers = ["VTotal", "VPercent Used", "VAvailable", "VUsed", "VFree", "STotal", "SPercent Used", "SUsed", "SFree", "SIN", "SOUT"]
            try:
                with open(self.fullpath, "a+") as file:
                    print("Saving to file")
                    filewriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    if self.hasHeader is False:
                        filewriter.writerow(headers)
                        self.hasHeader = True
                    else:
                        if len(rows) != 0:
                            #filewriter.writerows(rows)
                            print("printed rows")
            except Exception as ex:
                print(ex)
        return

    def Update_Data(self, data):
        self.data.append(data)
        return

    def Clear_Date(self):
        self.data = []
        return