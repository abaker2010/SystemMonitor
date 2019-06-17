#!/usr/bin/python
# Wrote by: Aaron Baker

import psutil
from .Converters import *

class Network:

    networkIO = None
    networkSentBytesDifferent = []

    def __init__(self):
        self.networkIO = psutil.net_io_counters()
        return

    '''
        - bytes_sent: number of bytes sent
        - bytes_recv: number of bytes received
        - packets_sent: number of packets sent
        - packets_recv: number of packets received
        - errin: total number of errors while receiving
        - errout: total number of errors while sending
        - dropin: total number of incoming packets which were dropped
        - dropout: total number of outgoing packets which were dropped (always 0 on macOS and BSD)
    '''

    def Pretty_Print_Network_IO(self):
        print(" -------------------------------------------------------------------------------")
        print(" -                                 Network I/O                                 -")
        print(" -------------------------------------------------------------------------------")
        print("\t%s\t\t%s %8.0f\t\t%s %9.0f" % ("Bytes:", "Sent: ", self.networkIO.bytes_sent, "Received: ", self.networkIO.bytes_recv))
        print("\t%s\t%s %8.0f\t\t%s %9.0f" % ("Packets:", "Sent: ", self.networkIO.packets_sent, "Received: ", self.networkIO.packets_recv))
        print(" -------------------------------------------------------------------------------\n")
        return


    def Print_Change(self):
        print(" -------------------------------------------------------------------------------")
        print(" -                            Network I/O (Changes)                            -")
        print(" -------------------------------------------------------------------------------")

        print(" -------------------------------------------------------------------------------")
        return

    def Update_Print(self):
        self.networkIO = psutil.net_io_counters()
        self.Pretty_Print_Network_IO()
        return