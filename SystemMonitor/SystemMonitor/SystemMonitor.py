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

def usage():
    parser.print_help()
    return

parser.add_option("-a", "--AVERAGE", dest="opt_average",
                  help="Usage: [True | False]    This option needs will create the averages of the collected information from the system", default=False)
parser.add_option("-c", "--COLLECT", dest="opt_collect",
                  help="Usage: [True | False]    This option will collect the systems performance information", default=True)
parser.add_option("-t", "--TYPE", dest="opt_type",
                  help="Usage: [True | False]    This option will collect the systems performance information", default=True)
parser.add_option("-i", "--INFECTED", dest="opt_infected",
                  help="Usage: [True | False]    This is to determine if it is a not/infected baseline", default=False)
parser.add_option("-L", "--LOOPS", dest="opt_loops",
                  help="Usage: INT   This will be used for counting the number of loops so that the csv lengths are the same", default=10)
parser.add_option("-F", "--FOLDER", dest="opt_folder",
                   help="Usage: [CPU | Disks | Memory | Network] This is to create averages of all the items in a dir with -i", default=None)
parser.add_option("-f", "--FILE", dest="opt_files",
                 help="Useage: [FILE1 FILE2] This will load in files to compare", nargs=2, default=[None, None])
parser.add_option("-g", "--GRAPH", dest="opt_graph",
                  help="Usage: [True | False] This will allow graphs to be generated", default=False)
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

    if bool(options.opt_graph) is True:
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
        if bool(options.opt_graph) is True:
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

    print("Exiting...\n\n")
    
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
        if bool(options.opt_graph) is True:
            #dGraph.Generate(infected={'Read-Count': [815915, 815915, 815915, 815915, 815915], 'Write-Count': [699143, 699660, 699661, 699666, 699668], 'Read-Bytes': [15900165632, 15900165632, 15900165632, 15900165632, 15900165632], 'Write-Bytes': [11911129088, 11915614208, 11915618304, 11915638784, 11915646976], 'Read-Time': [378, 378, 378, 378, 378], 'Write-Time': [282, 282, 282, 282, 282]})
            #nGraph.Generate()
            #mGraph.Generate(infected={'Virtual': {'Total': [17058402304, 17058402304, 17058402304, 17058402304, 17058402304, 17058402304], 'Percent': [40.6, 40.6, 40.7, 40.7, 40.7, 40.7], 'Available': [10134278144, 10132340736, 10120212480, 10117718016, 10123915264, 10120773632], 'Used': [6924124160, 6926061568, 6938189824, 6940684288, 6934487040, 6937628672], 'Free': [10134278144, 10132340736, 10120212480, 10117718016, 10123915264, 10120773632]}, 'Swap': {'Total': [19608539136, 19608539136, 19608539136, 19608539136, 19608539136, 19608539136], 'Percent': [38.0, 38.0, 38.0, 38.0, 38.0, 38.0], 'Used': [7447928832, 7449624576, 7460311040, 7459016704, 7450656768, 7460564992], 'Free': [12160610304, 12158914560, 12148228096, 12149522432, 12157882368, 12147974144], 'SIN': [0, 0, 0, 0, 0, 0], 'SOUT': [0, 0, 0, 0, 0, 0]}})
            mGraph.Generate()
            #cGraph.Generate()

    except Exception as e:
        print(e)
        exit(0)

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
    print(" Graph: %s" % bool(options.opt_graph))
    print(" ------------------------" + Style.RESET_ALL)
    return

if __name__ == "__main__":
    global Path
    global Infected
    colorama.init() 
    Path = os.path.dirname(os.path.abspath(__file__))
    
    Show_Args()
    
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
        if bool(options.opt_average) is False and bool(options.opt_collect) is True:
            Main()
        else:
            Generate_Averages()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully()

