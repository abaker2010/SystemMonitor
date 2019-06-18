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

# Global Defs
lMemory = None
wrMemory = None

lNetwork = None
wrNetwork = None

lCPU = None
wrCPU = None

lDisk = None
wrDisk = None

lDisplayThread = None
Path = None

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
    wrMemory.Update_Data(lMemory)
    wrCPU.Update_Data(lCPU)
    wrDisk.Update_Data(lDisk)
    wrNetwork.Update_Data(lNetwork)

    # Writing to files
    wrMemory.Save_Info()
    wrCPU.Save_Info()
    wrDisk.Save_Info()
    wrNetwork.Save_Info()

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

    try:
        Path = os.path.dirname(os.path.abspath(__file__))

        # Checking/Creating Folders
        fileStruct = FileStruct(Path)
        fileStruct.Check_Folders()

        # Setting up Memory and Memory Writer
        lMemory = Memory()
        wrMemory = Writer(Path + "\\CSV\\Memory\\", "Memory", None)
        # Setting up CPU and CPUs Writer
        lCPU = CPU(platform.system)
        wrCPU = Writer(Path + "\\CSV\\CPU\\", "CPU", None)
        # Setting up Disks and Disks Writer
        lDisk = Disks()
        wrDisk = Writer(Path + "\\CSV\\Disks\\", "Disk", None)
        # Setting up Network and Networks Writer
        lNetwork = Network()
        wrNetwork = Writer(Path + "\\CSV\\Network\\", "Network", None)
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
        print("Exit gracefully")

