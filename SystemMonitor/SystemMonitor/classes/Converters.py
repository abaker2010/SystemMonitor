#!/usr/bin/python
# Wrote by: Aaron Baker

import math

class Converters:

    def __init__(self):
        return

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%4.2f %s" % (s, size_name[i])
   