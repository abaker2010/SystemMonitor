#!/usr/bin/python
# Wrote by: Aaron Baker

import psutil
from .Converters import *

class Memory:

    virtualMemory = None
    swapMempry = None 

    def __init__(self):
        self.virtualMemory = psutil.virtual_memory()
        self.swapMempry = psutil.swap_memory()

        return

    '''
        - total: total physical memory
        - available: the memory that can be given instantly to processes without the system going into swap. 
                     This is calculated by summing different memory values depending on the platform and it is supposed 
                     to be used to monitor actual memory usage in a cross platform fashion.

        Other metrics:
        - used: memory used, calculated differently depending on the platform and designed for informational 
                purposes only. total - free does not necessarily match used.
        - free: memory not being used at all (zeroed) that is readily available note that this doesnt 
                reflect the actual memory available (use available instead). total - used does not necessarily
                match free.
        - active (UNIX): memory currently in use or very recently used, and so it is in RAM.
        - inactive (UNIX): memory that is marked as not used.
        - buffers (Linux, BSD): cache for things like file system metadata.
        - cached (Linux, BSD): cache for various things.
        - shared (Linux, BSD): memory that may be simultaneously accessed by multiple processes.
        - slab (Linux): in-kernel data structures cache.
        - wired (BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk.
    '''

    def Pretty_Print_Virtual_Memory(self):
        print(" --------------------------------------------------------------------------")
        print(" -                             Virtual Memory                             -")
        print(" --------------------------------------------------------------------------")
        print("\t%s     %s\t\t%s %s%s" % ("Total: ", Converters().convert_size(self.virtualMemory.total), "Percent Used: ", self.virtualMemory.percent, "%"))
        print("\t%s %s\t\t%s\t%s" % ("Available: ", Converters().convert_size(self.virtualMemory.available), "Used: ", Converters().convert_size(self.virtualMemory.used)))
        print("\t%s      %s" % ("Free: ", Converters().convert_size(self.virtualMemory.free)))
        print(" --------------------------------------------------------------------------\n")
        return
    
    '''
        - total: total swap memory in bytes
        - used: used swap memory in bytes
        - free: free swap memory in bytes
        - percent: the percentage usage calculated as (total - available) / total * 100
        - sin: the number of bytes the system has swapped in from disk (cumulative)
        - sout: the number of bytes the system has swapped out from disk (cumulative)
    '''

    def Pretty_Print_Swap_Memory(self):
        print(" --------------------------------------------------")
        print(" -                 Swap Memory                    -")
        print(" --------------------------------------------------")
        print("\t%s %s\t%s %s%s" % ("Total: ", Converters().convert_size(self.swapMempry.total), "Percent Used: ", self.swapMempry.percent, "%"))
        print("\t%s  %s\t\t%s %s" % ("Used: ", Converters().convert_size(self.swapMempry.used), "Free: ", Converters().convert_size(self.swapMempry.free)))
        print("\t%s   %s\t\t%s %s" % ("SIN: ", Converters().convert_size(self.swapMempry.free), "SOUT: ", Converters().convert_size(self.swapMempry.free)))
        print(" --------------------------------------------------\n")
        return
