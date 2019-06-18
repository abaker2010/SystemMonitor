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

    def __init__(self, dir, subfolder, data):
        self.dir = dir
        self.data = data
        self.filename = subfolder + "-" + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + ".csv"
        self.fullpath = self.dir + self.filename
        return
    
    def Save_Info(self):
        print(self.dir)
        print(self.filename)
        print(self.fullpath)
        if type(self.data) is CPU:
            print("CPU TYPE")
        elif type(self.data) is Network:
            print("Network TYPE")
        elif type(self.data) is Disks:
            print("Disks TYPE")
        elif type(self.data) is Memory:
            print("Memory TYPE")
        try:
            with open(self.fullpath, "a+") as file:
                print("Created file")
        except Exception as ex:
            print(ex)
        return

    def Update_Data(self, data):
        self.data = data
        return