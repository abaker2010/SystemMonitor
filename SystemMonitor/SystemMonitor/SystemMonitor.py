#!/usr/bin/python
# Wrote by: Aaron Baker

from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU
from classes.RepeatedTimer import RepeatedTimer
from classes.Writer import Writer
from classes.FileStruct import FileStruct

import os
import platform
import time
import datetime
import copy

def Display():
    global lMemory
    global wrMemory

    global lNetwork
    global wrNetwork

    global lCPU
    global wrCPU

    global lDisk
    global wrDisk

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

def main():
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
    global currentDate
    try:
        Path = os.path.dirname(os.path.abspath(__file__))
        currentDate = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
        # Checking/Creating Folders
        Files = FileStruct(Path)
        Files.Check_Folders()

        # Setting up Memory and Memory Writer
        lMemory = Memory()
        wrMemory = Writer(Path + "\\CSV\\Memory\\", "Memory", None, currentDate)
        # Setting up CPU and CPUs Writer
        lCPU = CPU(platform.system)
        wrCPU = Writer(Path + "\\CSV\\CPU\\", "CPU", None, currentDate)
        # Setting up Disks and Disks Writer
        lDisk = Disks()
        wrDisk = Writer(Path + "\\CSV\\Disks\\", "Disk", None, currentDate)
        # Setting up Network and Networks Writer
        lNetwork = Network()
        wrNetwork = Writer(Path + "\\CSV\\Network\\", "Network", None, currentDate)
        # Setting up the display thread
        lDisplayThread = RepeatedTimer(3, Display)
    except Exception as ex:
        print(ex)

    while True:
        time.sleep(1000)
    return


def exit_gracefully():
    global lDisplayThread
    lDisplayThread.stop()
    return

if __name__ == "__main__":
    try:        
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully()

