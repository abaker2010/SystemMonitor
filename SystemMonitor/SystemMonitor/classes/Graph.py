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

    global layout

    def __init__(self, type, xlabel, ylabel, title, grid):
        global layout
        layout = { "Infected" : {},
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
        print("\n   [-] Generating Graph")
        infected = kwargs.get("infected", None)
        #print(infected)
        X = list(self.data.keys())
        graphs = {}

        if self.type is CPU:
            print("Multi Graphs: CPU")
            for k, v in self.data.items():
                print(k)
                print(v.To_CSV_Array())
        elif self.type is Network:
            print("Multi Graphs: Network")
            graphs = self.Generate_Layout_2D(True, self.data)
            #graphs = self.Generate_Layout_2D(False, self.data)
            
            self.Plot_Graph_2D(X, graphs)
        elif self.type is Disks:
            print("Multi Graphs: Disks")
            print(self.data)
            graphs = self.Generate_Layout_2D(True, self.data)
            graphs = self.Generate_Layout_2D(False, self.data)
            graphs["Infected"] = infected
            print(graphs)
            self.Plot_Graph_2D(X, graphs)
        elif self.type is Memory:
            print("Multi Graphs: Memory")
           # graphs = self.Generate_Layout_3D(True, self.data)
            graphs = self.Generate_Layout_3D(False, self.data)
            #graphs["Infected"] = infected
            print(graphs)
            self.Plot_Graph_3D(X, graphs)
        print("   [-] Generated/Show Graph")
        
        return
    def Generate_Layout_3D(self, isInfected, objt):
        global layout
        isInfected = "Infected" if isInfected is True else "Not-Infected"
        for k, v in objt.items():
            for n, d in v.Graph_Output().items():
                if n not in layout[isInfected].keys():
                    layout[isInfected][n] = {}
                for t, val in d.items():
                    if t not in layout[isInfected][n].keys():
                        layout[isInfected][n][t] = []
                    layout[isInfected][n][t].append(val)
        return layout

    def Generate_Layout_2D(self, isInfected, objt):
        global layout
        isInfected = "Infected" if isInfected is True else "Not-Infected"
        for k, v in objt.items():
            for n, d in v.Graph_Output().items():
                if n not in layout[isInfected].keys():
                    layout[isInfected][n] = []
                layout[isInfected][n].append(d)
        print(layout)
        print("\n")
        return layout

    def Plot_Graph_2D(self, X, graphs):
        count = 0
        infected = True if bool(graphs["Infected"]) is True else False
        noninfected = True if bool(graphs["Not-Infected"]) is True else False
        data = graphs["Not-Infected"] if noninfected is True else graphs["Infected"]
        for k, v in data.items():
                plt.figure(num=count, figsize=(10,10))
                plt.xlabel(self.xlabel)
                plt.ylabel(self.ylabel)
                plt.title(k)
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

    def Plot_Graph_3D(self, X, graphs):
        count = 0
        infected = True if bool(graphs["Infected"]) is True else False
        noninfected = True if bool(graphs["Not-Infected"]) is True else False
        data = graphs["Not-Infected"] if noninfected is True else graphs["Infected"]
        for k, v in data.items():
               for n, d in v.items():
                   plt.figure(num=count, figsize=(10,10))
                   plt.title(k + " / " + n)
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