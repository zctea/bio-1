#!/usr/bin/pthon2.6
"""
processing the Gene data

!!! the input data are pure float numbers, and not metainfo!!!!
get rid of them before you call this program!

"",     gene_0, gene_1,gene_2,
-------------------------
"s0" | 1.0,  2.0,  3.0
"s1" | 3.0,  4.0,  ...
"s2" | ...

"""


import sys,os
from optparse import OptionParser
from operator import itemgetter
from sets import Set
import csv
import numpy as np

class DataProc:
    def __init__(self):
        self.fname = ""

    def loadcsv(self,fname):
        """ load .csv data file and store into a numpy array """
        self.fname = fname
        dot_pos = str.rfind(self.fname,".")
        if dot_pos is not 0:
            self.fname = self.fname[:dot_pos]
        data =  np.genfromtxt(fname, dtype=float,delimiter=",")
        return data

    def pcc(self,fname):
        data = self.loadcsv(fname) 
        matdata = np.asmatrix(data) #transfer to numpy matrix
        E = matdata.mean(1) #expectation
        SD = matdata.std(1) #standard deviation
        #print E
        #print SD
        print "Data Matrix shape: "+ str(matdata.shape)
        matshape = matdata.shape
        
        for i in range(matshape[0]):
            for j in range(matshape[1]): 
                if SD[i] != 0.0 :
                    matdata[i,j] = (matdata[i,j] - E[i]) / SD[i]
                    #print str(i) + str(j) + str(matdata[i,j])
                    
        #result = np.absolute(matdata * matdata.T) # absolute PCC
        result = matdata * matdata.T # PCC
        result = result / int(matshape[1]-1) # divided by number of samples 

        ## minus the identity matrix
        #for i in range(result.shape[0]):
            #result[i,i] = 0.0
        
        np.savetxt(self.fname+".pcc",result,delimiter=",",fmt="%1.5f")
        print "Result PCC Matrix shape: "+ str(result.shape)

    def topvalue(self,fname,numtops):
        """ load the top 'numtops' pairs fron datai matrix """ 
        data = self.loadcsv(fname)
        """ stupid method below """
        ### make a copy of the data 
        ds = data.shape
        values = [] 
        for j in range(0,ds[0]):
            for i in range(j+1,ds[1]):
                values.append((data[i,j],i,j))
        
        top_value = sorted(values,key=itemgetter(0),reverse=True)[:int(numtops)]

        ### dump top values
        f = open(self.fname+".topvalues","w")
        for p in top_value:
            f.write(str(p))
            f.write(os.linesep)
        f.close()

        ### write gene IDs ###
        top_id = Set() 
        for i in range(0,len(top_value)):
            top_id.add(top_value[i][1])
            top_id.add(top_value[i][2])

        f = open(self.fname+".top",'w')
        for i in top_id:
            f.write("%s\n" %  i)
        f.close()
        """
        genes = []
        for i in range(0,len(data)):
            genes.append((np.amax(data[i]),i))
        t = sorted(genes,key=itemgetter(0),reverse=True)[:int(numtops)]
        f = open(self.fname+".top",'w')
        for i in t:
            f.write("%s\n" % i[1])
        f.close()
        """
        

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f","--file",dest="filename",help="imput file name", metavar = "FILE")
    parser.add_option("-p","--pcc",action="store_true",dest="pcc",help="pearson correlation coefficient",metavar="PCC")
    parser.add_option("-s","--sort",action="store_true",dest="sort",help="sort the value of matrix element")

    (options,args) = parser.parse_args()

    if options.filename is None:
        print "error, no input file name!"
        parser.print_help()
        sys.exit(-1)
    
    if options.pcc is True:
        dp = DataProc()
        dp.pcc(options.filename)

    if options.sort is True:
        dp = DataProc()
        dp.topvalue(options.filename,50)
