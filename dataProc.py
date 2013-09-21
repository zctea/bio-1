#!/usr/bin/python
"""
processing the Microarray Expression Dataset 

an example of dataset:

"",     sample1, sample_2,sample_3,
"gene1"  1.0,  2.0,  3.0
"gene2"  3.0,  4.0,  ...
"gene3"  ...

shuchu.han@gmail.com
"""

import sys,os
from optparse import OptionParser
from operator import itemgetter
##from sets import Set
import csv
import numpy as np

class DataProc:
    def __init__(self):
        self.fname = ""
        self.genes = []
        self.samples = []
        self.data = ""

    def loadcsv(self,fname):
        """ 
          Load the .csv file in two run.
          1) first run:
            load the gene names and sample names
          2) second run:
            load the data by using the numpy.genfromtxt()
        """
        
        # get the the base file namne
        self.fname = fname
        dot_pos = str.rfind(self.fname,".")
        if dot_pos is not 0:
            self.fname = self.fname[:dot_pos]
        
        # load gene names and sample names
        with open(str(fname),'rb') as csvfile:
          f = csv.reader(csvfile,delimiter=',')
          first_line_flag = True
          for row in f:
            line_field = row
            if first_line_flag:
              self.samples = line_field
              first_line_flag = False
            else:
              self.genes.append(line_field[0])
        
        # load the data to numpy by using genfromtxt()
        # skip the first row, and the first column
        self.data = np.genfromtxt(fname, dtype=float,delimiter=",",\
                                  skip_header=1,usecols = range(1,len(self.samples)-1))
        return 0                          

    def save_genes(self):
      sample_fname = self.fname + '_samles.csv'
      with open(sample_fname,'wb') as csvfile:
        f = csv.writer(csvfile,delimiter=',')
        f.writerow(self.samples)  ## wirte the samples name to the first row
      
      genes_fname = self.fname + '_genes.csv'
      with open(genes_fname,'wb') as csvfile:
        f = csv.writer(csvfile,delimiter=',')
        f.writerow(self.genes)  ## wirte the samples name to the first row
      
      data_fname = self.fname + '_data.csv'
      np.savetxt(data_fname,self.data,fmt='%10.4f',delimiter=',')
      return 0
        
    def clean_dup_genes(self,method):
      """
        For each duplicated genes, keep the one with largest SD, remove others.
      """

      unwanted_lines = []
      len_of_genes = len(self.genes)
      for i in range(0,len_of_genes):
        checking_item = self.genes[i]
        dup_list = [i]
        for j in range(i+1,len_of_genes):
          if self.genes[j] == checking_item:
            dup_list.append(j)
        
        if len(dup_list) > 1:
            alived_line = -1 
            if method == "SD":
              alived_line = self._highest_SD(dup_list)
            
            if alived_line != -1:
              dup_list.remove(alived_line)
            
            if len(dup_list) > 0:
                for k in dup_list:
                    unwanted_lines.append(k)   

      # now removing
      print "Number of lines to be deleted from array: %d\n" % len(unwanted_lines)
      self.data = np.delete(self.data,unwanted_lines,0)
      new_genes = []
      for id, item in enumerate(self.genes):
          if unwanted_lines.count(id) == 0:
              new_genes.append(item)
      self.genes = new_genes
      return 0

    def _highest_SD(self,dup_list):
      """
        Find the line which has highest SD
      """
      max_index = -1
      if len(dup_list) > 0:
        SD = []
        for i in dup_list:
          line = self.data[i]
          sd = np.std(line)
          SD.append(SD)
        
        max_index = SD.index(max(SD))

      return dup_list[max_index]

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f","--file",dest="filename",help="imput file name", metavar = "FILE")
    parser.add_option("-c","--clean",action="store_true",dest="clean_dup_genes",\
                      help="clean the duplicate genes")
   
    (options,args) = parser.parse_args()

    if options.filename is None:
        print "error, no input file name!"
        parser.print_help()
        sys.exit(-1)
    
    if options.clean_dup_genes is True:
        dp = DataProc()
        dp.loadcsv(options.filename)
        dp.clean_dup_genes("SD")
        dp.save_genes()

