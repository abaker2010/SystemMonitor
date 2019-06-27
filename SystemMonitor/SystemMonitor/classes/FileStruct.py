#!/usr/bin/python
# Wrote by: Aaron Baker
import os
import platform

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
        print("[*] Checking Folder Structure")
        for f in self.folders:
            path = self.path + f
            if(platform.system() != "Windows"):
                path = path.replace("\\", "/")

            if not os.path.exists(path):
                os.makedirs(path)
                print("\t[-] Creating Folder " + path)
            else:
                print("\t[-] Folder Exists " + path)
        return
        