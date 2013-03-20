#!/usr/bin/python

"""
Download the GEO data from http://www.ncbi.nlm.nih.gov by using 
the information from the SOFT file.
here focus on the series data:
!Platform_series_id=GSE***
"""

import urllib
import sys,os
from optparse import OptionParser

class SoftParser:
    def __init__(self):
       self.samples = []
       self.series = []
       self.filename = None

    def parserID(self,filename):
        """ store the filename"""
        self.filename = os.path.basename(filename)
        """ parse the Samples ID and Series ID"""
        with open(filename,'r') as softfile:
            for line in softfile:
                if line[0] == '!':
                    field = line.strip().split("=")
                    if str(field[0]).strip() == '!Platform_sample_id':
                        self.samples.append(field[1].strip())
                    elif str(field[0]).strip() == '!Platform_series_id':
                        self.series.append(field[1].strip())

    def saveSamples(self):
        f = open(self.filename + '_sm.txt','w')
        for i in range(len(self.samples)):
            f.write(str(self.samples[i]) + '\n')
        f.close()
    
    def saveSeries(self):
        f = open(self.filename + '_se.txt','w')
        for i in range(len(self.series)):
            f.write(str(self.series[i]) + '\n')
        f.close()
    
    def buildDownloadList(self):
        """ build the HTTP download list and save it to a file"""
        fold_name = ""
        f = open(self.filename + '_list.txt','w')
        for gse in self.series:
            len_dig_id = len(gse) - 3  ## number of digitals in GSE****
            #print len_dig_id
            if len_dig_id == 3 :
                fold_name = "GSEnnn"
            elif len_dig_id == 4:
                fold_name = gse[:4] + "nnn"
            elif len_dig_id == 5:
                fold_name = gse[:5] + "nnn"
            addr = "ftp://ftp.ncbi.nlm.nih.gov/geo/series/" \
                    + fold_name + '/'+ str(gse) + '/suppl/'  \
                    + str(gse)  \
                    + '_RAW.tar' 
            f.write(addr + '\n')
        f.close()

class DownloadGeoData:
    """ obsoleted code """
    def __init__(self):
        self.samples_http_link = "http://www.ncbi.nlm.nih.gov/geosuppl/?" 
        self.series_http_link = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?"

    def download(self,filename):
        """ will download sample IDs or series IDs in filename"""
        f = open(filename,'r')
        for line in f:
            ID = line.strip()
            addr = "acc=" 
            fname =""
            if ID[2] == 'M':
                addr += str(ID) + "&file=" + str(ID) + ".CEL.gz"
                addr = self.samples_http_link + addr
                fname = str(ID) + ".CEL.gz"
            elif ID[2] == 'E':
                addr += str(ID)
                addr = self.series_http_link + addr
                fname = str(ID) + ".tar"
            os.system('wget %s -O %s -a download.log' % (addr,fname)) #call wget
            #os.system('curl -O %s' % addr) #call wget

        f.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f","--file",dest="filename",help="imput file name", metavar = "FILE")
    parser.add_option("-p","--parse",action="store_true",dest="parse",default=False, \
                        help="parse the samples data or series data from SOFT file.")
    parser.add_option("-d","--download",dest="download",action="store_true",default=False,\
                        help="download the samples or series data with IDs from input file.")
    (options,args) = parser.parse_args()

    if options.filename is None:
        print "error, no input file name!"
        parser.print_help()
        sys.exit(-1)
      
    if options.parse is True:  
       sp = SoftParser()
       sp.parserID(options.filename)
       sp.saveSeries()
       sp.saveSamples()
       sp.buildDownloadList()

    if options.download is True:
       dl = DownloadGeoData()
       dl.download(options.filename)
        
