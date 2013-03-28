#!/usr/bin/python 
"""
Process the GEO dataset file.
the format of data file is:

""    gene1 gene2 gene3 ...... geneN
GSMID  1.0   2.0   3.0   ...... 4.0
GSMID  2.0   3.0   4.0   ...... 5.0
"""

import sys
import csv
import numpy as np
from optparse import OptionParser
import os

class GeoFile:
    def __init__(self):
        self.file_basename =""
        self.data = [] 
        self.shape = ()
        self.gsmID = {}
        self.geneID = {} 

    def load_file(self,file_name):
        """ load .csv data file and store into list """
        self.file_basename = str(file_name).strip().split('.')[0]
        with open(str(file_name),'rb') as csvfile:
             f = csv.reader(csvfile,delimiter=',')
             for row in f:
                self.data.append(row)
        """ calcualte the shape of data """
        self.shape = (len(self.data),len(self.data[0]))
        self.split_metainfo()

        print "data shape: " + str(self.shape)

    def split_metainfo(self):   
        if self.data != None:
            """ dump the first row """
            for i in range(1,self.shape[1]):
                self.geneID[self.data[0][i]] = i
                #print self.data[0][i]

            """ dump the first column"""
            for j in range(1,self.shape[0]):
                self.gsmID[self.data[j][0]] = j
                #print self.data[j][0]

    def dump_metainfo(self):
        if len(self.geneID) != 0:
            """ split the first row """ 
            row_file = open(self.file_basename + ".geneID", "w")
            """ dump the first row """
            for k in self.geneID.keys():
                row_file.write("%s,%i\n" %(k,self.geneID[k]))
            row_file.close()

        if len(self.gsmID) != 0:
            col_file = open(self.file_basename + ".gsmID","w")
            for k in self.gsmID.keys():
                col_file.write("%s,%i\n" % (k,self.gsmID[k]))
            col_file.close()

    def dump_data(self):
        """ dump the data matrix from data file """
        f = open(self.file_basename + ".mat","wb")
        wf = csv.writer(f,dialect='excel')
        for i in range(1,len(self.data)):
            wf.writerow(self.data[i])
        f.close()

    def dump_genes(self,gene_fname):
        """ dump the sample data of genes which are listed in 
            file gene_fname, assume the gene list file only
            has the name of genes, no other strings.
        """
        f = open(gene_fname,"r")
        gene_list = []
        for gene in f:
            gene_list.append(gene.strip())
        f.close()
      
        #find the column position of genes
        gene_pos = []
        for gene in gene_list:
            #if self.geneID.has_key(str(gene)):
             gene_pos.append(self.geneID[str(gene)])
        print len(gene_pos)

        gf = open(self.file_basename + '.gene',"wb")
        gf_csv = csv.writer(gf,dialect='excel')
        for i in range(self.shape[0]):
            line = []
            #print self.data[i][0]
            line.append(self.data[i][0])
            for  index in gene_pos:
                line.append(self.data[i][index])
            gf_csv.writerow(line)
        gf.close()

    def dump_gene_from_list(self,gene_fname):
        f = open(gene_fname,"r")
        gene_list = []
        for gene in f:
            gene_list.append(gene.strip())
        f.close()
        pos_of_dot = str.rfind(gene_fname,'.')
        gf_basename = gene_fname
        if pos_of_dot is not 0:
            gf_basename = gene_fname[:pos_of_dot]
        gf = open(gf_basename + '.gene',"wb")
        f = open(gf_basename+".glist","w")
        gf_csv = csv.writer(gf,dialect='excel')
        for gene in gene_list:
            gf_csv.writerow(self.data[int(gene)+1])
            f.write("%s\n" % (self.data[int(gene)+1])[0])
        f.close()
        gf.close()
    
    def transpose(self):
        t_data = zip(*self.data)
        tf = open(self.file_basename + ".t","wb")
        #tf_cw = csv.writer(tf,dialect='excel',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        tf_cw = csv.writer(tf,dialect='excel')
        for row in t_data:
            tf_cw.writerow(row)
        tf.close()

    def merge(self):
        print os.getcwd()
        
        mf = open("merge.csv","w")
        
        head = 1
        for  f in os.listdir("."):
            if f.endswith(".gene"):
                tf = open(f,"r")
                if head == 1:
                    head = 0  #write the head
                else:
                    tf.next()
                for line in tf:
                    mf.write(line)
                tf.close() 
        mf.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f","--file",dest="filename",help="imput file name", metavar = "FILE")
    parser.add_option("-t","--transpose",action="store_true",dest="transpose",help="transpose the matrix in file")
    parser.add_option("-d","--dump_data",action="store_true",dest="dump_data",help="dump the data matrix only(remove metainfo)")
    parser.add_option("-g","--dump_gene",dest="genelist",help="dump the sample data of listed genes ID in file")
    parser.add_option("-n","--dump_gene_by_name",dest="genename",help="dump the sample data of listed genes NAME in file")
    parser.add_option("-m","--metainfo",action="store_true",dest="metainfo",help="dump the metainfo of dataset")
    parser.add_option("-c","--merge",action="store_true",dest="merge",help="merge all the .gene file to a single file")
    parser.add_option("-i","--info",action="store_true",dest="info",help="show info")

    (options,args) = parser.parse_args()

    if options.transpose is True:
        gf = GeoFile()
        gf.load_file(options.filename)
        gf.transpose()

    if options.dump_data is True:
        gf = GeoFile()
        gf.load_file(options.filename)
        gf.dump_data()
    
    if options.metainfo is True:
        gf = GeoFile()
        gf.load_file(options.filename)
        gf.dump_metainfo()

    if options.genelist is not None:
        gf = GeoFile()
        gf.load_file(options.filename)
        gf.dump_gene_from_list(options.genelist)

    if options.genename is not None:
        gf = GeoFile()
        gf.load_file(options.filename)
        gf.dump_genes(options.genename)
    
    if options.merge is True:
        gf = GeoFile()
        gf.merge()

    if options.info is True:
        gf = GeoFile()
        gf.load_file(options.filename)
