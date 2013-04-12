#!/usr/bin/python 

import sys
import csv

"""
given an Expression table, mapping the probe id at each ROW
to gene id. 

fileOne --- Expression table. (CSV format)
pid_gid_file --- a pid gid mapping file. (CSV format)
"""

def pid2gid(fileOne,pid_gid_file):
    data = csv.reader(fileOne,delimiter=',')
    pid_gid = csv.reader(pid_gid_file,delimiter=",")
    

    
    
