from classes.Memory import Memory
from classes.Disks import Disks
from classes.Network import Network
from classes.CPU import CPU
import os
import platform
import time

while True:
    memory = Memory()
    memory.Pretty_Print_Virtual_Memory()
    memory.Pretty_Print_Swap_Memory()

    cpu = CPU(platform.system())
    cpu.Pretty_Print_CPU_Times()

    diskUsage = Disks()
    #diskUsage.Pretty_Print_Disk_Info()
    #diskUsage.Pretty_Print_Disk_Usage()
    diskUsage.Pretty_Print_Disk_IO()

    networkUsage = Network()
    networkUsage.Pretty_Print_Network_IO()

    time.sleep(4)

    if(platform.system() == "Windows"):
        os.system('cls')
    else:
        os.system('clear')

