#!/usr/bin/python
# Wrote by: Aaron Baker

from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU
from classes.RepeatedTimer import RepeatedTimer
from classes.Writer import Writer
from classes.FileStruct import FileStruct
from classes.CommandOpts import CommandOpts
from classes.Reader import Reader
from classes.Averages import Averages
from classes.Graph import Graph
import colorama 
from colorama import Fore, Back, Style

# Graphing
import matplotlib.pyplot as plt
# -----------------------------

import os
import platform
import time
import datetime
import copy
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--AVERAGE", dest="opt_average",
                  help="Usage: [True | False]    This option needs will create the averages of the collected information from the system", default=False)
parser.add_option("-c", "--COLLECT", dest="opt_collect",
                  help="Usage: [True | False]    This option will collect the systems performance information", default=True)
parser.add_option("-t", "--TYPE", dest="opt_type",
                  help="Usage: [True | False]    This option will collect the systems performance information", default=True)
parser.add_option("-i", "--INFECTED", dest="opt_infected",
                  help="Usage: [True | False]    This is to determin if it is a not/infected baseline")
options, args = parser.parse_args()

def usage():
    parser.print_help()
    return



def Display():
    global lMemory
    global wrMemory

    global lNetwork
    global wrNetwork

    global lCPU
    global wrCPU

    global lDisk
    global wrDisk

    global dGraph
    global nGraph
    global mGraph
    global cGraph

    if(platform.system() == "Windows"):
        os.system('cls')
    else:
        os.system('clear')

    # Updating system information
    lMemory.Update()
    lCPU.Update()
    lDisk.Update()
    lNetwork.Update()
    
    # Updating writers
    timeStamp = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())

    wrMemory.Update_Data({timeStamp : copy.deepcopy(lMemory)})
    wrCPU.Update_Data({timeStamp : copy.deepcopy(lCPU)})
    wrDisk.Update_Data({timeStamp : copy.deepcopy(lDisk)})
    wrNetwork.Update_Data({timeStamp : copy.deepcopy(lNetwork)})
    
    dGraph.Add_Point(timeStamp, copy.deepcopy(lDisk))
    nGraph.Add_Point(timeStamp, copy.deepcopy(lNetwork))
    mGraph.Add_Point(timeStamp, copy.deepcopy(lMemory))
    cGraph.Add_Point(timeStamp, copy.deepcopy(lCPU))

    # Writing to files 
    # this needs to happen only when the arrays are say X loops are done
    # in the writing it will need to create an array with the data 
    # also when save info is called it will need to clear the data
    wrMemory.Save_Info()
    wrCPU.Save_Info()
    wrDisk.Save_Info()
    wrNetwork.Save_Info()
    
    wrMemory.Clear_Date()
    wrCPU.Clear_Date()
    wrDisk.Clear_Date()
    wrNetwork.Clear_Date()

    # Printing Updated Values
    lMemory.Print()
    lCPU.Print()
    lDisk.Print()
    lNetwork.Print()
    return

def Main():
    global lMemory
    global wrMemory

    global lNetwork
    global wrNetwork

    global lCPU
    global wrCPU

    global lDisk
    global wrDisk

    global lDisplayThread
    global Path 
    global Files
    global Infected
    global currentDate

    global dGraph
    global nGraph
    global mGraph
    global cGraph

    try:
        currentDate = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
        
        # Setting up Memory and Memory Writer
        lMemory = Memory()
        infected = "Infected" if Infected is True else "Not-Infected"
        print(Path + "\\CSV\\Memory\\" + infected  + "\\")
        wrMemory = Writer(Path + "\\CSV\\Memory\\" + infected  + "\\", "Memory", None, currentDate)
        # Setting up CPU and CPUs Writer
        lCPU = CPU(platform.system)
        wrCPU = Writer(Path + "\\CSV\\CPU\\" + infected  + "\\", "CPU", None, currentDate)
        # Setting up Disks and Disks Writer
        lDisk = Disks()
        wrDisk = Writer(Path + "\\CSV\\Disks\\" + infected  + "\\", "Disk", None, currentDate)
        # Setting up Network and Networks Writer
        lNetwork = Network()
        wrNetwork = Writer(Path + "\\CSV\\Network\\" + infected + "\\", "Network", None, currentDate)

        # Setting up graph objects
        dGraph = Graph(Disks, "Time", "Value", "Disk Performance", True)
        nGraph = Graph(Network, "Time", "Value", "Network Performance", True)
        mGraph = Graph(Memory, "Time", "Value", "Memory Performance", True)
        cGraph = Graph(CPU, "Time", "Value", "CPU Performance", True)


        # Setting up the display thread
        lDisplayThread = RepeatedTimer(3, Display)
    except Exception as ex:
        print(ex)

    while True:
        time.sleep(1000)
    return

def Generate_Averages():
    global Path
    global Infected

    print(Fore.LIGHTCYAN_EX + "  Generate Averages" + Fore.GREEN)
    try:
        try:
            memoryReader = Reader(Memory, None, Infected)
            memoryReader.Read_CSV()
            memoryAverage = Averages(memoryReader)
            memoryAverage.Filter_Data()
            memoryAverage.Get_Averages()

            memoryAverageWriter = Writer(Path + "\\Averages\\Memory\\", "Memory", memoryAverage, "Averages")
            memoryAverageWriter.Save_Averages()
        except Exception as em:
            print("Memory Average Error")
            print(em)

        try:
            diskReader = Reader(Disks, None, Infected)
            diskReader.Read_CSV()
            diskAverage = Averages(diskReader)
            diskAverage.Filter_Data()
            diskAverage.Get_Averages()
            
            diskAverageWriter = Writer(Path + "\\Averages\\Disks\\", "Disks", diskAverage, "Averages")
            diskAverageWriter.Save_Averages()
        except Exception as ed:
            print("Disk Average Error")
            print(ed)
        
        try:
            netReader = Reader(Network, None, Infected)
            netReader.Read_CSV()
            netAverage = Averages(netReader)
            netAverage.Filter_Data()    
            netAverage.Get_Averages()
            
            netAverageWriter = Writer(Path + "\\Averages\\Network\\", "Network", netAverage, "Averages")
            netAverageWriter.Save_Averages()
        except Exception as en:
            print("Network Average Error")
            print(en)

        try:
            cpuReader = Reader(CPU, None, Infected)
            cpuReader.Read_CSV()
            cpuAverage = Averages(cpuReader)
            cpuAverage.Filter_Data()
            cpuAverage.Get_Averages()
            
            cpuAverageWriter = Writer(Path + "\\Averages\\CPU\\", "CPU", cpuAverage, "Averages")
            cpuAverageWriter.Save_Averages()
        except Exception as ec:
            print("CPU Average Error")
            print(ec)

    except Exception as e:
        print(e)
    
    return

def exit_gracefully():
    global lDisplayThread
    global dGraph
    global nGraph
    global mGraph
    global cGraph

    print("Exiting...\n\n")
    
    try:
        lDisplayThread.stop()
    except Exception as e:
        print(e)

    try:
        Generate_Averages()
    except Exception as e:
        print(e)

    try:
        dGraph.Generate()
        nGraph.Generate()
        mGraph.Generate(infected={'Virtual': {'Total': [17058402304, 17058402304, 17058402304, 17058402304], 'Percent': [49.2, 49.3, 49.3, 49.3], 'Available': [8659337216, 8649359360, 8645390336, 8645005312], 'Used': [8399065088, 8409042944, 8413011968, 8413396992], 'Free': [8659337216, 8649359360, 8645390336, 8645005312]}, 'Swap': {'Total': [19608539136, 19608539136, 19608539136, 19608539136], 'Percent': [48.8, 48.9, 48.9, 48.9], 'Used': [9577721856, 9580658688, 9591209984, 9585778688], 'Free': [10030817280, 10027880448, 10017329152, 10022760448], 'SIN': [0, 0, 0, 0], 'SOUT': [0, 0, 0, 0]}})
        #mGraph.Generate()
        cGraph.Generate()
    except Exception as e:
        print(e)
        exit(0)

    return

if __name__ == "__main__":
    global Path
    global Infected
    colorama.init() 
    Path = os.path.dirname(os.path.abspath(__file__))
    print(Fore.GREEN + " ------------------------")
    print("\t\tOptions")
    print(" Average: %s" % options.opt_average)
    print(" Collect: %s" % options.opt_collect)
    print(" Type: %s" % options.opt_type)
    print(" Infected?: %s" % options.opt_infected)
    print(" ------------------------" + Style.RESET_ALL)
    
    if bool(options.opt_average) != False | bool(options.opt_average) != True:
        usage()
        exit(0)

    if bool(options.opt_collect) != False | bool(options.opt_collect) != True:
        usage()
        exit(0)
    if bool(options.opt_type) != False | bool(options.opt_type) != True:
        usage()
        exit(0)
    if bool(options.opt_infected) != False | bool(options.opt_infected) != True:
        usage()
        exit(0)

    # Checking/Creating Folders
    Files = FileStruct(Path)
    Files.Check_Folders()
    Infected = True if options.opt_infected == "True" else False

    #Infected = "Infected" if bool(options.opt_infected) is True else "Not-Infected"
    print(Infected)
    try:       
        if options.opt_average == False:
            Main()
        else:
            Generate_Averages()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully()

