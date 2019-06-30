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
from classes.AverageReader import AverageReader
from classes.Recollect import Recollect
from classes.Averages import Averages
from classes.Graph import Graph
import colorama 
from colorama import Fore, Back, Style

# Graphing
import matplotlib.pyplot as plt
# -----------------------------

import os
import sys
import platform
import time
import datetime
import copy
from optparse import OptionParser

parser = OptionParser()

def usage():
    parser.print_help()
    return

parser.add_option("-a", "--AVERAGE", dest="opt_average",
                  help="Usage: [True | FALSE]    This option needs will create the averages of the collected information from the system", default=False)
parser.add_option("-c", "--COLLECT", dest="opt_collect",
                  help="Usage: [True | FALSE]    This option will collect the systems performance information", default=False)
parser.add_option("-C", "--COMPARE", dest="opt_compare",
                  help="Usage: [True | FALSE]    This option will compare collect the systems performance information", default=False)
parser.add_option("-t", "--TYPE", dest="opt_type",
                  help="Usage: [TRUE | False]    This option will collect the systems performance information", default=True)
parser.add_option("-i", "--INFECTED", dest="opt_infected",
                  help="Usage: [True | FALSE]    This is to determine if it is a not/infected baseline", default=False)
parser.add_option("-L", "--LOOPS", dest="opt_loops",
                  help="Usage: INT   This will be used for counting the number of loops so that the csv lengths are the same (Default: 10)", type=int, default=10)
parser.add_option("-F", "--FOLDER", dest="opt_folder",
                   help="Usage: [CPU | Disks | Memory | Network] This is to specify the folder main folder to compare files: -f needed with this command", default=None)
parser.add_option("-f", "--FILE", dest="opt_files",
                 help="Useage: <NON-INFECTED> <INFECTED> This will load in files to compare", nargs=2, default=[None, None])
parser.add_option("-g", "--GRAPH", dest="opt_graph",
                  help="Usage: [True | FALSE] This will allow graphs to be generated", default=False)
options, args = parser.parse_args()
    
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
    global LoopsAllowed
    global LoopCount

    if LoopCount < (LoopsAllowed - 1):
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

        if options.opt_graph is True:
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
    
        wrMemory.Clear_Data()
        wrCPU.Clear_Data()
        wrDisk.Clear_Data()
        wrNetwork.Clear_Data()

        # Printing Updated Values
        lMemory.Print()
        lCPU.Print()
        lDisk.Print()
        lNetwork.Print()
        LoopCount += 1
    else:
        lDisplayThread.stop()
        print(Fore.LIGHTYELLOW_EX + " [!] System Done Collecting Please Press CTRL+C To Finish" + Style.RESET_ALL)
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
    global LoopCount
    global LoopsAllowed

    try:
        currentDate = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
        
        # Setting up Memory and Memory Writer
        lMemory = Memory()
        infected = "Infected" if Infected is True else "Not-Infected"
        wrMemory = Writer(Path + "\\CSV\\Memory\\" + infected  + "\\", "Memory", None, currentDate)
        # Setting up CPU and CPUs Writer
        lCPU = CPU()
        wrCPU = Writer(Path + "\\CSV\\CPU\\" + infected  + "\\", "CPU", None, currentDate)
        # Setting up Disks and Disks Writer
        lDisk = Disks()
        wrDisk = Writer(Path + "\\CSV\\Disks\\" + infected  + "\\", "Disk", None, currentDate)
        # Setting up Network and Networks Writer
        lNetwork = Network()
        wrNetwork = Writer(Path + "\\CSV\\Network\\" + infected + "\\", "Network", None, currentDate)

        LoopsAllowed = options.opt_loops
        LoopCount = 0
        # Setting up graph objects
        if options.opt_graph is True:
            dGraph = Graph(Disks, "Time", "Value", "Disk Performance", True)
            nGraph = Graph(Network, "Time", "Value", "Network Performance", True)
            mGraph = Graph(Memory, "Time", "Value", "Memory Performance", True)
            cGraph = Graph(CPU, "Time", "Value", "CPU Performance", True)


        # Setting up the display thread
        lDisplayThread = RepeatedTimer(1, Display)
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
    global lDisk

    try:
        lDisplayThread.stop()
    except Exception as e:
        print(e)
    try:
        if options.opt_average is True:
            Generate_Averages()
    except Exception as e:
        print(e)

    try:
        # option for infection needs to be added
        # Another check will need to be added to see if there is infected information to 
        # pass in to the system for graphing
        if options.opt_graph is True:
            dGraph.Generate()
            nGraph.Generate()
            mGraph.Generate()
            cGraph.Generate()
        
    except Exception as e:
        print(e)
    
    print(Fore.LIGHTCYAN_EX + "\n Good Bye :) \n\n" + Style.RESET_ALL)
    sys.exit()
    return

def Show_Args():
    print(Fore.GREEN + " ------------------------")
    print("\t\tOptions")
    print(" Average: %s" % options.opt_average)
    print(" Collect: %s" % options.opt_collect)
    print(" Type: %s" % options.opt_type)
    print(" Infected?: %s" % options.opt_infected)
    print(" Files: %s  %s" % (str(options.opt_files[0]), str(options.opt_files[1])))
    try:
        print(" Folders: %s " % options.opt_folder)
    except:
        print(" Folders: Not Specified")
    print(" Graph: %s" % options.opt_graph)
    print(" ------------------------" + Style.RESET_ALL)
    return

def Option_Check():
    if str(options.opt_average).lower() == 'true':
        options.opt_average = True
    elif str(options.opt_average).lower() == 'false':
        options.opt_average = False
    elif str(options.opt_average).lower() != 'false' | str(options.opt_average) != 'true':
        usage()
        exit(0)
       
    if str(options.opt_collect).lower() == 'true':
        options.opt_collect = True
    elif str(options.opt_collect).lower() == 'false':
        options.opt_collect = False
    elif str(options.opt_collect).lower() != 'false' | str(options.opt_collect) != 'true':
        usage()
        exit(0)

    if str(options.opt_type).lower() == 'true':
        options.opt_type = True
    elif str(options.opt_type).lower() == 'false':
        options.opt_type = False
    elif str(options.opt_type).lower() != 'false' | str(options.opt_type) != 'true':
        usage()
        exit(0)

    if str(options.opt_infected).lower() == 'true':
        options.opt_infected = True
    elif str(options.opt_infected).lower() == 'false':
        options.opt_infected = False
    elif str(options.opt_infected).lower() != 'false' | str(options.opt_infected) != 'true':
        usage()
        exit(0)

    if str(options.opt_graph).lower() == 'true':
        options.opt_graph = True
    elif str(options.opt_graph).lower() == 'false':
        options.opt_graph = False
    elif str(options.opt_graph).lower() != 'false' | str(options.opt_graph) != 'true':
        usage()
        exit(0)

    if str(options.opt_compare).lower() == 'true':
        options.opt_compare = True
    elif str(options.opt_compare).lower() == 'false':
        options.opt_compare = False
    elif str(options.opt_compare).lower() != 'false' | str(options.opt_compare) != 'true':
        usage()
        exit(0)
    return

if __name__ == "__main__":
    global Path
    global Infected
    colorama.init() 
    Path = os.path.dirname(os.path.abspath(__file__))
    
    Option_Check()
    Show_Args()

    # Checking/Creating Folders
    Files = FileStruct(Path)
    Files.Check_Folders()
    Infected = True if options.opt_infected is True else False

    try:       
        if options.opt_collect is True:
            Main()
        elif options.opt_average is True and options.opt_compare is False:
            Generate_Averages()
        elif options.opt_compare is True:
            if options.opt_folder is None:
                usage()
                sys.exit()
            elif options.opt_files is not None:
                folder = options.opt_folder
                files = options.opt_files
                folder = folder.lower()
                if folder == 'cpu' or folder == 'disks' or folder == 'memory' or folder == 'network':
                    if folder == 'cpu':
                        fType = CPU
                    elif folder == 'disks':
                        fType = Disks
                    elif folder == 'memory':
                        fType = Memory
                    elif folder == 'network':
                        fType = Network

                    comparer = Recollect(fType, ("\CSV\%s\\Not-Infected\%s" % (folder, files[0])), False)
                    comparer.Read()
                    comparer.Change_File(("\CSV\%s\\Infected\%s" % (folder, files[1])))
                    comparer.Change_Infected(True)
                    comparer.Read()

                    if fType is Disks:
                        dGraph = Graph(fType, "Time", "Value", "Disk Performance", True)
                        dGraph.Plot_Graph_2D(comparer.Graph_X(), comparer.Get_Graph())
                    elif fType is Network:
                        nGraph = Graph(fType, "Time", "Value", "Network Performance", True)
                        nGraph.Plot_Graph_2D(comparer.Graph_X(), comparer.Get_Graph())
                    elif fType is Memory:
                        mGraph = Graph(fType, "Time", "Value", "Memory Performance", True)
                        mGraph.Plot_Graph_3D(comparer.Graph_X(), comparer.Get_Graph())
                    elif fType is CPU:
                        nGraph = Graph(fType, "Time", "Value", "CPU Performance", True)
                        nGraph.Plot_Graph_2D(comparer.Graph_X(), comparer.Get_Graph())
                else:
                    usage()
    except KeyboardInterrupt:
        exit_gracefully()

