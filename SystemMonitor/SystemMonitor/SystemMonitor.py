#!/usr/bin/python
# Wrote by: Aaron Baker

from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU
from classes.RepeatedTimer import RepeatedTimer
import os
import platform
import time

# Global Defs
lMemory = None
lNetwork = None
lCPU = None
lDisk = None
lDisplayThread = None

def Display():
    global lMemory
    global lNetwork
    global lCPU
    global lDisk

    if(platform.system() == "Windows"):
        os.system('cls')
    else:
        os.system('clear')

    lMemory.Update_Print()
    lCPU.Update_Print()
    lDisk.Update_Print()
    lNetwork.Update_Print()
    return

def main():
    global lMemory
    global lNetwork
    global lCPU
    global lDisk
    global lDisplayThread
    try:
        lMemory = Memory()
        lCPU = CPU(platform.system)
        lDisk = Disks()
        lNetwork = Network()
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

