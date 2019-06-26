#!/usr/bin/python
# Wrote by: Aaron Baker

import psutil
import platform
from .Converters import *
import colorama 
from colorama import Fore, Back, Style

class CPU:

    def __init__(self, system):
        self.cpuTimes = psutil.cpu_times(percpu=True)
        self.systemType = system
        self.coreCount = len(self.cpuTimes)
        return

    def Get_Core_Count(self):
        return self.coreCount
    def Get_Info(self):
        return self.cpuTimes

    def Update(self):
        self.cpuTimes = psutil.cpu_times(percpu=True)
        return 

    def Print(self):
        self.Pretty_Print_CPU_Times()
        return 

    '''
        - user: time spent by normal processes executing in user mode; on Linux this also includes guest time
        - system: time spent by processes executing in kernel mode
        - idle: time spent doing nothing

        Platform Specific:
        - nice (UNIX): time spent by niced (prioritized) processes executing in user mode;
                       on Linux this also includes guest_nice time
        - iowait (Linux): time spent waiting for I/O to complete
        - irq (Linux, BSD): time spent for servicing hardware interrupts
        - softirq (Linux): time spent for servicing software interrupts
        - steal (Linux 2.6.11+): time spent by other operating systems running in a virtualized environment
        - guest (Linux 2.6.24+): time spent running a virtual CPU for guest operating systems 
                                 under the control of the Linux kernel
        - guest_nice (Linux 3.2.0+): time spent running a niced guest 
                                     (virtual CPU for guest operating systems under the control of the Linux kernel)
        - interrupt (Windows): time spent for servicing hardware interrupts ( similar to irq on UNIX)
        - dpc (Windows): time spent servicing deferred procedure calls (DPCs); 
                         DPCs are interrupts that run at a lower priority than standard interrupts.
    '''

    def Pretty_Print_CPU_Times(self):
        print(Fore.LIGHTGREEN_EX + " --------------------------------------------------")
        print(" -" + Fore.CYAN + "                 CPU Time                       " + Fore.LIGHTGREEN_EX + "-")
        print(Fore.LIGHTGREEN_EX + " --------------------------------------------------" + Style.RESET_ALL)
        cpuCount = 0
        for cpu in self.cpuTimes:
            cpuCount += 1
            print(Fore.LIGHTYELLOW_EX + "\t%s %.0f" % ("CPU: ", cpuCount))
            print(Fore.GREEN + "\t--------" + Style.RESET_ALL)            
            print(Fore.LIGHTCYAN_EX + "\t%s %6.0f\t%s    %4.0f" % ("User: ", cpu.user, "System: ", cpu.system))
            try:
                print("\t%s  %6.0f\t%s %4.0f" % ("Idle:", cpu.idle, "Interrupt: ", cpu.interrupt))
            except:
                print("\t%s  %6.0f\t%s %4.0f" % ("Idle:", cpu.idle, "Interrupt: ", 0))
            try:
                print("\t%s  %6.0f\n" % ("DPC: ", cpu.dpc))
            except:
                print("\t%s  %6.0f\n" % ("DPC: ", 0))
        print(Fore.LIGHTGREEN_EX + " --------------------------------------------------\n" + Style.RESET_ALL)
        return

    def To_CSV_Array(self):
        csv = {}
        # user, system, idle, interrupt, dpc
        count = 1
        for cpu in self.cpuTimes:
            try:
                csv[count] = [cpu.user, cpu.system, cpu.idle, cpu.interrupt, cpu.dpc]
            except:
                csv[count] = [cpu.user, cpu.system, cpu.idle, 0, 0]
            count += 1
        return csv