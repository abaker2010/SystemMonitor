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


# Graphing
import matplotlib.pyplot as plt
import numpy as np
# -----------------------------

class Graph:
    # Reference 
    # https://pythonspot.com/matplotlib-line-chart/


    def __init__(self, type, xlabel, ylabel, title, grid):
        
        self.layout = { "Infected" : {},
                   "Not-Infected" : {}}
        self.data = {}
        self.type = type
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.grid = grid
        return

    def Add_Point(self, time, obj):
        self.data[time] = obj
        return

    def Generate(self, *args, **kwargs):
        
        infected = kwargs.get("infected", False)
        infectedObj = kwargs.get("infectedObj", None)
        X = list(self.data.keys())
        graphs = {}

        if self.type is CPU:
            print(Fore.LIGHTCYAN_EX + "\n   [-] Generating Graph : CPU" + Style.RESET_ALL)
            graphs = self.Generate_Layout_3D(False, self.data)
            self.Plot_Graph_3D(X, graphs)
        elif self.type is Network:
            print(Fore.LIGHTCYAN_EX + "\n   [-] Generating Graph : Network" + Style.RESET_ALL)
            graphs = self.Generate_Layout_2D(infected, self.data)
            self.Plot_Graph_2D(X, graphs)
        elif self.type is Disks:
            print(Fore.LIGHTCYAN_EX + "\n   [-] Generating Graph : Disks" + Style.RESET_ALL)
            if infected is False:
                graphs = self.Generate_Layout_2D(False, self.data) # Repeat this if the infected object exits pass it on next call
            else:
                graphs = self.Generate_Layout_2D(False, self.data)
                graphs["Infected"] = infectedObj
            self.Plot_Graph_2D(X, graphs)
        elif self.type is Memory:
            print(Fore.LIGHTCYAN_EX + "\n   [-] Generating Graph : Memory" + Style.RESET_ALL)
            graphs = self.Generate_Layout_3D(infected, self.data)
            self.Plot_Graph_3D(X, graphs)
        return

    def Generate_Layout_3D(self, isInfected, objt):
        isInfected = "Infected" if isInfected is True else "Not-Infected"
        for k, v in objt.items():
            for n, d in v.Graph_Output().items():
                if n not in self.layout[isInfected].keys():
                    self.layout[isInfected][n] = {}
                for t, val in d.items():
                    if t not in self.layout[isInfected][n].keys():
                        self.layout[isInfected][n][t] = []
                    self.layout[isInfected][n][t].append(val)
        return self.layout

    def Plot_Graph_3D(self, X, graphs):
        count = 0
        infected = True if bool(graphs["Infected"]) is True else False
        noninfected = True if bool(graphs["Not-Infected"]) is True else False
        data = graphs["Not-Infected"] if noninfected is True else graphs["Infected"]
        for k, v in data.items():
               for n, d in v.items():
                   plt.figure(num=count, figsize=(10,10))
                   plt.title(self.title + "  " + k + " / " + n)
                   plt.xlabel(self.xlabel)
                   plt.ylabel(self.ylabel)
                   plt.grid(self.grid)
                   labelText = "Not-Infected" if noninfected is True else "Infected"
                   colorInfo = "blue" if noninfected is True else "red"
                   if noninfected is True and infected is True:
                       plt.plot(X, graphs["Infected"][k][n], label="Infected", color="red")
                   plt.plot(X, d, label=labelText, color=colorInfo)
                   plt.legend()
                   count += 1
               plt.show() 
        return

    def Generate_Layout_2D(self, isInfected, objt):
        isInfected = "Infected" if isInfected is True else "Not-Infected"
        for k, v in objt.items():
            for n, d in v.Graph_Output().items():
                if n not in self.layout[isInfected].keys():
                    self.layout[isInfected][n] = []
                self.layout[isInfected][n].append(d)
        return self.layout

    def Plot_Graph_2D(self, X, graphs):
        count = 0
        infected = True if bool(graphs["Infected"]) is True else False
        noninfected = True if bool(graphs["Not-Infected"]) is True else False
        data = graphs["Not-Infected"] if noninfected is True else graphs["Infected"]
        for k, v in data.items():
                plt.figure(num=count, figsize=(10,10))
                plt.xlabel(self.xlabel)
                plt.ylabel(self.ylabel)
                plt.title(self.title + "  " + k)
                plt.grid(self.grid)
                labelText = "Not-Infected" if noninfected is True else "Infected"
                colorInfo = "blue" if noninfected is True else "red"
                if noninfected is True and infected is True:
                    plt.plot(X, graphs["Infected"][k], label="Infected", color="red")
                plt.plot(X, v, label=labelText, color=colorInfo)
                plt.legend()
                count += 1
        plt.show()
        return

   