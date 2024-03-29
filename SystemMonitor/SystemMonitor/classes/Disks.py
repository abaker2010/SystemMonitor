#!/usr/bin/python
# Wrote by: Aaron Baker

import psutil
import psutil
from .Converters import *
import colorama 
from colorama import Fore, Back, Style

class Disks:

    # This will need to be edited so that it will work with all hard drives that
    # have been found and not just the first one
    # We need to monitor all of the hard drives for activity

    def __init__(self):
        self.diskPartitions = psutil.disk_partitions()[0]
        self.diskUsage = psutil.disk_usage(self.diskPartitions.device)
        self.diskIO = psutil.disk_io_counters()
        return  
    
    def Update(self):
        self.diskUsage = psutil.disk_usage(self.diskPartitions.device)
        self.diskIO = psutil.disk_io_counters()
        return

    def Print(self):
        self.Pretty_Print_Disk_IO()
        return

    '''
        - read_count: number of reads
        - write_count: number of writes
        - read_bytes: number of bytes read
        - write_bytes: number of bytes written

        Platform Specific fields:

        - read_time: (all except NetBSD and OpenBSD) time spent reading from disk (in milliseconds)
        - write_time: (all except NetBSD and OpenBSD) time spent writing to disk (in milliseconds)
        - busy_time: (Linux, FreeBSD) time spent doing actual I/Os (in milliseconds)
        - read_merged_count (Linux): number of merged reads
        - write_merged_count (Linux): number of merged writes 
    '''

    def Pretty_Print_Disk_Info(self):
        print(" --------------------------------------------------")
        print(" -                 Disk Info                      -")
        print(" --------------------------------------------------")
        print("\t%s %s\t%s %s" % ("Device: ", self.diskPartitions.device, "Mount Point: ", self.diskPartitions.mountpoint))
        print("\t%s %s\t%s %s" % ("Type: ", self.diskPartitions.fstype, "Opts: ", self.diskPartitions.opts))
        print(" --------------------------------------------------\n")
        return

    def Pretty_Print_Disk_Usage(self):
        print(" --------------------------------------------------")
        print(" -                 Disk Usage                     -")
        print(" -                 {}                            -".format(self.diskPartitions.device))
        print(" --------------------------------------------------")
        print("\t%s %s\t%s %s" % ("Total: ", Converters().convert_size(self.diskUsage.total), "Used: ", Converters().convert_size(self.diskUsage.used)))
        print("\t%s %s\t%s %s%s" % ("Free: ", Converters().convert_size(self.diskUsage.free), "Percent: ", self.diskUsage.percent, "%"))
        print(" --------------------------------------------------\n")
        return

    def Pretty_Print_Disk_IO(self):
        print(Fore.LIGHTGREEN_EX + " -------------------------------------------------------------------------------")
        print(" -" + Fore.CYAN + "                                Disk I/O                                     " + Fore.LIGHTGREEN_EX + "-")
        print(" -------------------------------------------------------------------------------" + Fore.LIGHTCYAN_EX)
        print("\t%s %11.0f\t%s %10.0f" % ("Read Count: ", self.diskIO.read_count, "Write Count: ", self.diskIO.write_count))
        print("\t%s %11.0f\t%s %10.0f" % ("Read Bytes: ", self.diskIO.read_bytes, "Write Bytes: ", self.diskIO.write_bytes))
        print("\t%s  %11.0f\t%s  %10.0f" % ("Read Time: ", self.diskIO.read_time, "Write Time: ", self.diskIO.write_time))
        print(Fore.LIGHTGREEN_EX + " -------------------------------------------------------------------------------\n" + Style.RESET_ALL)
        return 

    def To_CSV_Array(self):
        csv = []
        csv.append(self.diskIO.read_count)
        csv.append(self.diskIO.read_bytes)
        csv.append(self.diskIO.read_time)
        csv.append(self.diskIO.write_count)
        csv.append(self.diskIO.write_bytes)
        csv.append(self.diskIO.write_time)
        return csv

    def Graph_Output(self):
        graph = {}
        graph["Read-Count"] = self.diskIO.read_count
        graph["Write-Count"] = self.diskIO.write_count
        graph["Read-Bytes"] = self.diskIO.read_bytes
        graph["Write-Bytes"] = self.diskIO.write_bytes
        graph["Read-Time"] = self.diskIO.read_time
        graph["Write-Time"] = self.diskIO.write_time
        return graph