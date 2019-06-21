#!/usr/bin/python
# Wrote by: Aaron Baker
import os

class FileStruct:
    def __init__(self, path):
        self.path = path
        self.folders = folders = ["\\CSV", "\\CSV\\CPU", "\\CSV\\Disks", "\\CSV\\Network", "\\CSV\\Memory"]
        return
    
    def Check_Folders(self):
        print("[*] Checking Folder Structure")
        for f in self.folders:
            path = self.path + f
            if not os.path.exists(path):
                os.makedirs(path)
                print("\t[-] Creating Folder " + path)
            else:
                print("\t[-] Folder Exists " + path)

        return

    def Create_File(self):
        return