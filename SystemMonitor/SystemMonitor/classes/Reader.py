#!/usr/bin/python
# Wrote by: Aaron Baker

import csv
import os
import platform
import datetime
import copy
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU

class Reader:

    def __init__(self, type, date):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "\.."
        self.type = type
        self.date = date
        self.platform = platform.system()
        self.data = None
        self.folders = folders = ["\\CSV\\CPU\\", "\\CSV\\Disks\\", "\\CSV\\Network\\", "\\CSV\\Memory\\"]
        return
    
    def Get_Type(self):
        return self.type

    def Parse_Information(self,sub):
        Averages = {}
        lDir = self.path + self.folders[sub]
        if(platform.system() != "Windows"):
            lDir = lDir.replace("\\", "/")
        fileList = os.listdir(lDir)
        for file in fileList:
            Averages[file] = {}
            lFile = self.path + self.folders[sub] + file
            if(platform.system() != "Windows"):
                lFile = lFile.replace("\\", "/")
            with open(lFile, "r") as f:
                count = 0
                colCount = 0
                keys = []
                for line in f:
                    lineSplit = []
                    lineSplit = line.strip().split(',')
                    lineSplit.pop(0)
                    if count == 0:
                        count += 1
                        colCount = len(lineSplit)
                        keys = copy.deepcopy(lineSplit)
                        for k in lineSplit:
                            Averages[file][k] = []
                    else:
                        c = 0
                        while c < colCount:
                            val = keys[c]
                            Averages[file][val].append(float(lineSplit[c]))
                            c += 1
        return Averages

    def Read_CSV(self):
        
        if self.type is CPU:
            self.data = self.Parse_Information(0)
        elif self.type is Disks:
            self.data = self.Parse_Information(1)
        elif self.type is Network:
            self.data = self.Parse_Information(2)
        elif self.type is Memory:
            self.data = self.Parse_Information(3)
        return

    def Get_Info(self):
        return self.data
