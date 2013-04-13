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
    pg = {}
    data = []
   
    #load the probe ID to Gene ID
    f = csv.reader(pid_gid_file,delimiter=",",quotechar='\"')
    for row in f:
        print row
    
    #data = csv.reader(fileOne,delimiter=',')

if __name__ == "__main__":
    pid2gid(sys.argv[0],sys.argv[1])
