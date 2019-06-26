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
# -----------------------------

class Graph:
    # Reference 
    # https://pythonspot.com/matplotlib-line-chart/

    def __init__(self, type, xlabel, ylabel, title, grid):
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

    def Generate(self):
        print("\n   [-] Generating Graph")
        Y = [32,36]
        X = list(self.data.keys())
        
        if self.type is CPU:
            print("Multi Graphs: CPU")
        elif self.type is Network:
            print("Multi Graphs: Network")
        elif self.type is Disks:
            print("Multi Graphs: Disks")
        elif self.type is Memory:
            print("Multi Graphs: Memory")


        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.grid(self.grid)
        plt.plot(X,Y)
        print("   [-] Generated/Show Graph")
        plt.show()
        return