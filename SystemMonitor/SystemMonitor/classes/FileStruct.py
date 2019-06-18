#!/usr/bin/python
# Wrote by: Aaron Baker
import os

class FileStruct:
    path = None
    folders = ["\\CSV", "\\CSV\\CPU", "\\CSV\\Disks", "\\CSV\\Network", "\\CSV\\Memory"]

    def __init__(self, path):
        self.path = path
        return
    
    def Check_Folders(self):
        for f in self.folders:
            path = self.path + f
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                print("Folders Exist")

        return

    def Create_File(self):
        return