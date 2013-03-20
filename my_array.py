#!/usr/bin/pthon2.6

"""
process the microarray data.

the format of data file is:
!!!! caution!, this file format will abund
gene1 gene2 gene3 ...... geneN
1.0   2.0   3.0   ...... 4.0
2.0   3.0   4.0   ...... 5.0
...
...

"""
import sys,csv
import numpy as np

class MyArray:
    def __init__(self):
        self.fname = ""

    def loadcsv(self,fname):
        """ load .csv data file and store into a numpy array """
        self.fname = fname
        dot_pos = str.rfind(self.fname,".")
        self.fname = self.fname[:dot_pos]
        data =  np.genfromtxt(fname, dtype=float,delimiter=",")
        return data

    def normalize(self,fname):
        data = self.loadcsv(fname) 
        t_data = zip(*data)
        matdata = np.asmatrix(t_data) #transfer to numpy matrix
        E = matdata.mean(1) #expectation
        SD = matdata.std(1) #standard deviation
        print E
        print SD
        print matdata.shape
        matshape = matdata.shape
        for i in range(matshape[0]):
            print i
            for j in range(matshape[1]): 
                if SD[i] != 0.0 :
                    matdata[i,j] = (matdata[i,j] - E[i]) / SD[i]
   
        result = matdata * matdata.T # PCC
        np.savetxt("pcc.csv",result,delimiter=",")

    def PCC(self,fname):
        pass
    
    def dataframe(self,fname):
        """ obtain the data frame form a .csv file """
        inputfile = open(fname,"r")
        outputfile = open("dataframe.csv","w")
        
        for line in inputfile:
            field = line.strip().split(",")
            field.pop(0)
            for i in range(len(field)):
                if i != len(field) - 1 :
                    outputfile.write(field[i] + ",")
                else:
                    outputfile.write(field[i])
            outputfile.write("\n")

        inputfile.close()
        outputfile.close()


    def combine(self,fname1,fname2):
        """ combine two files together """
        f1 = csv.DictReader(open(fname1,'rb'),delimiter = ",")
        f2 = csv.DictReader(open(fname2,'rb'),delimiter = ",")
        
        fieldnames = f1.fieldnames

        merged_file = csv.DictWriter(open("merged.csv","ab"),delimiter=",",fieldnames=fieldnames)
        merged_file.writeheader()

        for row in f1:
            merged_file.writerow(row)
    
        for row in f2:
            merged_file.writerow(row)
       

if __name__ == "__main__":
    fname = sys.argv[1]
    my_array = MyArray()
    #my_array.dataframe(fname)
    #my_array.normalize(fname)
    my_array.combine(sys.argv[1],sys.argv[2])

        
