#!/usr/bin/python
# Wrote by: Aaron Baker

import csv
import os
import platform
from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU

class Recollect:
    def __init__(self, fType, file, infected):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "\.." + file
        self.data = None
        self.graph = {"Not-Infected" : {}, "Infected" : {}}
        self.infected = "Not-Infected" if infected is False else "Infected"
        self.X = []
        self.fType = fType
        return 

    def Read(self):
        if(platform.system() != "Windows"):
            self.path = self.path.replace("\\", "/")
        self.X = []
        ldata = []
        lineCount = 0
        with open(self.path, "r") as f:
            for line in f:
                ldata.append(line.strip().split(','))
                self.X.append(lineCount)
                lineCount += 1
        ldata.pop(0)
        self.X.pop(0)
        if self.fType is Disks:
            self.data = {
                    "Read-Count" : [],
                    "Write-Count" : [],
                    "Read-Bytes" : [],
                    "Write-Bytes" : [],
                    "Read-Time" : [],
                    "Write-Time" : []
                    }
        elif self.fType is Network:
            self.data = {
                    "Bytes-Sent" : [],
                    "Bytes-Recv" : [],
                    "Packets-Sent" : [],
                    "Packets-Recv" : []
                }
        elif self.fType is Memory:
            self.data = {
                    "Virtual" : {
                            "Total" : [],
                            "Percent" : [],
                            "Available" : [],
                            "Used" : [],
                            "Free" : []
                        },
                    "Swap" : {
                            "Total" : [],
                            "Percent" : [],
                            "Used" : [],
                            "Free" : [],
                            "SIN" : [],
                            "SOUT" : []
                        }
                }
        elif self.fType is CPU:
            self.data = {
                    "User" : [],
                    "System" : [],
                    "Idel" : [],
                    "Interrupt" : [],
                    "DPC" : []
                }
        self.graph[self.infected] = self.data

        for d in ldata:
            if self.fType is Disks:
                self.graph[self.infected]["Read-Count"].append(d[1])
                self.graph[self.infected]["Write-Count"].append(d[2])
                self.graph[self.infected]["Read-Bytes"].append(d[3])
                self.graph[self.infected]["Write-Bytes"].append(d[4])
                self.graph[self.infected]["Read-Time"].append(d[5])
                self.graph[self.infected]["Write-Time"].append(d[6])
            elif self.fType is Network:
                self.graph[self.infected]["Bytes-Sent"].append(d[1])
                self.graph[self.infected]["Bytes-Recv"].append(d[2])
                self.graph[self.infected]["Packets-Sent"].append(d[3])
                self.graph[self.infected]["Packets-Recv"].append(d[4])
            elif self.fType is Memory:
                self.graph[self.infected]["Virtual"]["Total"].append(d[1])
                self.graph[self.infected]["Virtual"]["Percent"].append(d[2])
                self.graph[self.infected]["Virtual"]["Available"].append(d[3])
                self.graph[self.infected]["Virtual"]["Used"].append(d[4])
                self.graph[self.infected]["Virtual"]["Free"].append(d[5])

                self.graph[self.infected]["Swap"]["Total"].append(d[6])
                self.graph[self.infected]["Swap"]["Percent"].append(d[7])
                self.graph[self.infected]["Swap"]["Used"].append(d[8])
                self.graph[self.infected]["Swap"]["Free"].append(d[9])
                self.graph[self.infected]["Swap"]["SIN"].append(d[10])
                self.graph[self.infected]["Swap"]["SOUT"].append(d[11])
            elif self.fType is CPU:
                self.graph[self.infected]["User"].append(d[1])
                self.graph[self.infected]["System"].append(d[2])
                self.graph[self.infected]["Idel"].append(d[3])
                self.graph[self.infected]["Interrupt"].append(d[4])
                self.graph[self.infected]["DPC"].append(d[5])
        return

    def Change_File(self, file):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "\.." + file
        return
    
    def Graph_X(self):
        return self.X

    def Change_Infected(self, infected):
        self.infected = "Not-Infected" if infected is False else "Infected"
        return 

    def Get_Graph(self):
        return self.graph