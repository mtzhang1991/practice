#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import os,sys
import argparse
from scipy import stats
#import seaborn as sns
import subprocess
'''
parser = argparse.ArgumentParser()
parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")
'''
def run(parser):
    args = parser.parse_args()


    ##need to install computeMatrix and add it to your ~/.bashrc file
    ##pass the python variables to subprocess

    ##need to install computeMatrix and add it to your ~/.bashrc file
    ##pass the python variables to subprocess
    subprocess.call("rm merge.ave.txt", shell=True)
    ##iterate multiple input files
    for i in range(len(args.bigwig)):

        subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i],args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, args.outFile[i]),shell=True)


    for i in range(len(args.bigwig)):
        subprocess.call("gunzip -f %s" % args.outFile[i], shell=True)


    for i in range(len(args.bigwig)):
        subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
    #subprocess.call("rm merge.ave.txt", shell=True)
    dt = pd.read_table("merge.ave.txt",header=None)
    #data = np.random.rand(7,24)
    #row_labels = ['5hmc','K4m1','K27ac','K4m3','K27m3','FAIRE','GRO','GRO']
    row_labels = [a for a in args.rowlabels]

    array= dt.as_matrix(columns=dt.columns[0:])
    print len(array)

    y=array
    #a=np.arange(len(array[0])).reshape(1,len(array[0]))
    #x=np.repeat(a,len(array),axis=0)
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    colours=['r','g','b','orange','c','m','orange','violet','lightpink']
    #plt.xlim(0, len(array[2]))
    #for i in range(len(x)):
        #fig=plt.figure()
    fig,ax = plt.subplots()
    plt.xlim(0,len(array[0]))
    for i in range(len(array)):
        plt.plot(x,y[i],colours[i],linewidth=3,label=args.rowlabels[i])
        #plt.legend(args.rowlabels[i],loc="upper left")
        plt.legend(loc="upper left")
        #print args.rowlabels[i]
        #ax=fig.get_figure()
    ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'])
    #plt.title(args.rowlabels[i])
    plt.xlabel('Regions Relative Positions')
    plt.ylabel('Signals')
    #fig.savefig(str(args.rowlabels[i])+".pdf")
    #fig.savefig("curveTest2.pdf")
    fig.savefig(args.pdfName +".pdf")
    #plt.show()


