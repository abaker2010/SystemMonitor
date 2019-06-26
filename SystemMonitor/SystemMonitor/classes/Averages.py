#!/usr/bin/python
# Wrote by: Aaron Baker

from classes.Reader import Reader
from classes.Writer import Writer
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU

class Averages:
    def __init__(self, reader):
        self.ReaderObj = reader
        self.filtered_data = {}
        self.averages = {}
        return

    def Filter_Data(self):
        info = self.ReaderObj.Get_Info()
        for f, fi in info.items():
            for k, v in fi.items():
                if k not in self.filtered_data.keys():
                    self.filtered_data[k] = v
                else:
                    self.filtered_data[k] += v
        return 
    
    def Get_Type(self):
        return self.ReaderObj.Get_Type()

    def Get_Averages(self):
        if not self.filtered_data:
            self.Filter_Data()
        for k, v in self.filtered_data.items():
            self.averages[k] = sum(v) / len(v)
        return
    
    def Save_Averages(self):
        dir = None
        val = []
        for k, v in self.averages.items():
            val.append(v)
        return val



