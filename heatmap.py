import sys
import numpy as np
import matplotlib.pyplot as plt

class DrawPlot:
    def __init__(self):
        pass

    def loadlistfile(self,fname):
        f = open(fname,'r')
        result = []
        for line in f:
            result.append(line.strip())
        f.close()
        return result

    """ 
        fname : data file name
        gname : gene names
    """
    def heatmap(self,fname,gname):
        bname = fname.strip().split('.')[0]
        data = np.loadtxt(fname,delimiter=',')
        names =  self.loadlistfile(gname)
        print data.shape
        fig,ax = plt.subplots()
        ax.pcolormesh(data)
        ax.set_xticks(np.arange(data.shape[0])+0.5,minor=False)
        ax.set_yticks(np.arange(data.shape[1])+0.5,minor=False)
        #ax.invert_yaxis()
        #ax.xaxis.tick_top()
        ax.set_xticklabels(names,minor=False,size=6,rotation=-90)
        ax.set_yticklabels(names,minor=False,size=6)
        #plt.show()
        plt.savefig(bname+'_heat.png')

if __name__ == '__main__':
    dp = DrawPlot()
    dp.heatmap(sys.argv[1],sys.argv[2])
        
