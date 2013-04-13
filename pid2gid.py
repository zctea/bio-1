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
    with open(pid_gid_file,'rb') as p:
        f = csv.reader(p,delimiter=",",quotechar='\"')
        for row in f:
            pg[row[1]] = row[2]

    """ load data """
    with open(fileOne,'rb') as q:
        f = csv.reader(q,delimiter=",")
        for row in f:
            data.append(row)

    """ mapping """
    for item in data:
        if pg.has_key(item[0]):
            item[0] = pg[item[0]]

    with open("mapped.csv",'wb') as r:
        wf = csv.writer(r,dialect='excel')
        for i in data:
            wf.writerow(i)

if __name__ == "__main__":
    pid2gid(str(sys.argv[1]),str(sys.argv[2]))
