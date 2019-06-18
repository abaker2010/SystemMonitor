#!/usr/bin/python
# Wrote by: Aaron Baker

import psutil
import platform
from .Converters import *

class CPU:

    cpuTimes = None
    systemType = None

    def __init__(self, system):
        self.cpuTimes = psutil.cpu_times(percpu=True)
        self.systemType = system
        return

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
        print(" --------------------------------------------------")
        print(" -                 CPU Time                       -")
        print(" --------------------------------------------------")
        cpuCount = 0
        for cpu in self.cpuTimes:
            cpuCount += 1
            print("\t%s %.0f" % ("CPU: ", cpuCount))
            print("\t--------")
            print("\t%s %6.0f\t%s    %4.0f" % ("User: ", cpu.user, "System: ", cpu.system))
            print("\t%s  %6.0f\t%s %4.0f" % ("Idle:", cpu.idle, "Interrupt: ", cpu.interrupt))
            print("\t%s  %6.0f\n" % ("DPC: ", cpu.dpc))

        #print("\t%s %s\t%s %s" % ("User: ", self.cpuTimes.user, "System: ", self.cpuTimes.system))
        #print("\t%s %s" % ("Idle", self.cpuTimes.idle))
        #print(self.cpuTimes)
        print(" --------------------------------------------------\n")
        return