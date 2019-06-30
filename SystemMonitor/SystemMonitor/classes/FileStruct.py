#!/usr/bin/python
# Wrote by: Aaron Baker
import os
import platform
import colorama 
from colorama import Fore, Back, Style

class FileStruct:
    def __init__(self, path):
        self.path = path
        self.folders = folders = ["\\CSV", "\\CSV\\CPU\\Infected", "\\CSV\\CPU\\Not-Infected", 
                                  "\\CSV\\Disks\\Infected", "\\CSV\\Disks\\Not-Infected", 
                                  "\\CSV\\Network\\Infected", "\\CSV\\Network\\Not-Infected", 
                                  "\\CSV\\Memory\\Infected", "\\CSV\\Memory\\Not-Infected", 
                                  "\\Averages", "\\Averages\\CPU", "\\Averages\\Disks" , "\\Averages\\Network", "\\Averages\\Memory"]
        return
    
    def Check_Folders(self):
        print(Fore.CYAN + "[*] Checking Folder Structure" + Style.RESET_ALL)
        for f in self.folders:
            path = self.path + f
            if(platform.system() != "Windows"):
                path = path.replace("\\", "/")

            if not os.path.exists(path):
                os.makedirs(path)
                print(Fore.LIGHTRED_EX + "\t[-] Creating Folder " + path + Style.RESET_ALL)
            else:
                print(Fore.LIGHTCYAN_EX + "\t[-] Folder Exists " + path + Style.RESET_ALL)
        return
        