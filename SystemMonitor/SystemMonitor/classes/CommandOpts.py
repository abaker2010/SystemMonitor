#!/usr/bin/python
# Wrote by: Aaron Baker
import enum

class CommandOpts(enum.Enum):
    Infected = True
    UnInfected = False
    Collect = True
    NoCollect = False
    Average = True
    NoAverage = False