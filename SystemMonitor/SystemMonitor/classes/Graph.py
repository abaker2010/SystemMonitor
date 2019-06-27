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

        X = list(self.data.keys())
        graphs = {}

        if self.type is CPU:
            print("Multi Graphs: CPU")
            for k, v in self.data.items():
                print(k)
                print(v.To_CSV_Array())
        elif self.type is Network:
            print("Multi Graphs: Network")

        elif self.type is Disks:
            print("Multi Graphs: Disks")
        elif self.type is Memory:
            print("Multi Graphs: Memory")
            graphs = {"Infected" : {
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
                                    },
                    "Not-Infected" : {
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
                      }
            for k, v in self.data.items():
                graphs["Not-Infected"]["Virtual"]["Total"].append(v.Virtual_Memory().total)
                graphs["Not-Infected"]["Virtual"]["Percent"].append(v.Virtual_Memory().percent)
                graphs["Not-Infected"]["Virtual"]["Available"].append(v.Virtual_Memory().available)
                graphs["Not-Infected"]["Virtual"]["Used"].append(v.Virtual_Memory().used)
                graphs["Not-Infected"]["Virtual"]["Free"].append(v.Virtual_Memory().free)

                graphs["Not-Infected"]["Swap"]["Total"].append(v.Swap_Memory().total)
                graphs["Not-Infected"]["Swap"]["Percent"].append(v.Swap_Memory().percent)
                graphs["Not-Infected"]["Swap"]["Used"].append(v.Swap_Memory().used)
                graphs["Not-Infected"]["Swap"]["Free"].append(v.Swap_Memory().free)
                graphs["Not-Infected"]["Swap"]["SIN"].append(v.Swap_Memory().sin)
                graphs["Not-Infected"]["Swap"]["SOUT"].append(v.Swap_Memory().sout)

            graphs["Infected"] = infected
            
            self.Plot_Show(X, graphs, infected)
                    
        print("   [-] Generated/Show Graph")
        
        return

    def Plot_Show(self, X, graphs, oObj):
            count = 0
            if oObj is None:
                for v in graphs["Not-Infected"]:
                    for m, l in graphs["Not-Infected"][v].items():
                        plt.figure(num=count, figsize=(10,10))
                        plt.xlabel(self.xlabel)
                        plt.ylabel(self.ylabel)
                        plt.title(v + " " + m)
                        plt.grid(self.grid)
                        plt.plot(X, l, label="Infected")
                        plt.legend()
                        plt.show()
                        count += 1
            else:
                for v in graphs["Not-Infected"]:
                    for m, l in graphs["Not-Infected"][v].items():
                        plt.figure(num=count, figsize=(10,10))
                        plt.xlabel(self.xlabel)
                        plt.ylabel(self.ylabel)
                        plt.title(v + " " + m)
                        plt.grid(self.grid)
                        plt.plot(X, graphs["Infected"][v][m], label="Infected", color="red")
                        plt.plot(X, l, label="Not-Infected", color="blue")
                        plt.legend()
                        plt.show()
                        count += 1
            return
    
        