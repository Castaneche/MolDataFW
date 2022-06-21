'''
Read h5 file generated with PubChem's json files and create .com files for Gaussian
.com files are stored inside separated folders
'''

import pandas as pd
import os
import sys
import glob
from Utils.PeriodicTable import * 
from Utils.utils import * 


def writeComFile(filename, data):
    with open(filename, 'w') as f:
        f.write(method + '\n')
        f.write('# units(au,deg)\n')
        f.write('\n')
        f.write(title + '\n')
        f.write('\n')
        #f.write(f'{int(data["charge"])}\t{int(data["multiplicity"])}\n')
        fstr='{:5d}\t{:d}\n'.format(int(data["charge"]),int(data["multiplicity"]))
        f.write(fstr)

        atoms = data['atoms']
        coords = data['coords']
        pt = PeriodicTable()
        for i in range(len(atoms)):
            fstr='{:5s} {:20.10f}  {:20.10f}  {:20.10f}\n'.format(pt.elementZ(atoms[i]).symbol, coords[(i*3)],coords[(i*3) + 1],coords[(i*3) + 2])
            f.write(fstr)

        f.write('\n')

def createComFiles(outputPatentDir, outputId, data):
        outputDir = outputParentDir + '/' + str(outputId)
        for i, row in data.iterrows():
           #Write a Gaussian file    
           writeComFile(outputDir + '/' + str(int(row['cid'])) + '.com', row)

def saveDataFrame(outputPatentDir, outputId, data):
        outputDir = outputParentDir + '/' + str(outputId)
        #Create folder to store N data
        # Check whether the specified path exists or not
        if os.path.exists(outputDir) == False:
            os.mkdir(outputDir)
        data.to_hdf(outputDir + '/'+str(outputId) + '.h5', 'df')
        #data.to_csv(outputDir + '/'+str(outputId) + '.csv',sep='\t')

def saveData(outputPatentDir, outputId, data):
        saveDataFrame(outputPatentDir, outputId, data)
        createComFiles(outputPatentDir, outputId, data)

def addData(data, df, numGeomBegin,numGeomEnd):
        if numGeomBegin > numGeomEnd:
            return data
        if data.empty :
            data = df.iloc[numGeomBegin:numGeomEnd+1]
        else:
            data = pd.concat([data, df.iloc[numGeomBegin:numGeomEnd+1]], join="inner")
        return data


args = getArgumentsCom()
nByBatch = args.N
soft = args.soft
method = args.params
title = 'File generated from  PubChemDB'


tmpIndex = 0
tmpData = pd.DataFrame()

outputParentDir = args.outdir

# Create outputParentDirectory
if os.path.exists(outputParentDir) == False:
     os.mkdir(outputParentDir)
    
files = sorted(glob.glob(args.h5dir+"/*.h5"))
numFile=0
numGeomBegin=0
numGeomEnd = numGeomBegin

#print("filename=",files[numFile])
df = pd.read_hdf(files[numFile], 'df')
nShape=df.shape[0]
data = pd.DataFrame()
n=1
outputId = 0
nSaved=0

#Default case for --N arg
#If none is specified then N is equal to the size of the .h5 input file
if nByBatch<1:
    N = df.shape[0]
    outputId = getFileOutName(files[numFile])
else:
    N = nByBatch

while True:
    #print("n=",n,"numBegin = ", numGeomBegin, "numEnd = ", numGeomEnd)
        
    #General case : we read N molecules in a single file, store them in a specific folder
    if n >= N:
        nSaved += n 
        '''
        print("nSaved=", nSaved)
        print("n=N : saveData n/N=",n,"/",N)
        print("numGFile=", numGeomBegin, "/", numGeomEnd," (last included)")
        '''
        data = addData(data, df, numGeomBegin,numGeomEnd) 
        '''
        #print("data=",data)
        print("df.shape=",df.shape)
        print("===========================")
        #print("filename=",files[numFile])
        '''
        saveData(outputParentDir, outputId, data)
        #Update the folder only if we have specified a custom --N arg
        if nByBatch>0:
            outputId += 1
        #reset
        data = pd.DataFrame()
        numGeomBegin = numGeomEnd+1
        n = 0

    n += 1

    #print("dfshape=", df.shape)
    #print("df=", df)

    #Special case : we are at the end of the current file and n < N 
    #we need to read the next file to get a total of N molecules
    if numGeomEnd >= df.shape[0]-1:
        numFile += 1
        #We reached the last file, save remaining data and exit
        if numFile >= len(files):
            if n >= 1:
                if numGeomBegin < numGeomEnd:
                    nSaved += n-1
                    '''
                    print("nSaved=", nSaved)
                    print("saveData n/N=",n,"/",N)
                    print("numGFile=", numGeomBegin, "/", numGeomEnd," (last included)")
                    print("df.shape=",df.shape)
                    print("===========================")
                    #print("filename=",files[numFile-1])
                    '''
                    data = addData(data, df, numGeomBegin,numGeomEnd) 
                #Save the remaining data and exit
                saveData(outputParentDir, outputId, data)
                break #We iterated over every .h5 files, stop the while loop
        #Switch to the next .h5 file and update all variables
        else: #note that this is where we land at the first iteration
            if numGeomBegin < numGeomEnd:
                #print("add, numGFile=", numGeomBegin, "/", numGeomEnd," (last included)")
                data = addData(data, df, numGeomBegin,numGeomEnd) 

            #print("filename=",files[numFile])
            df = pd.read_hdf(files[numFile], 'df') #extract dataframe from file
            nShape += df.shape[0]
            #reset
            numGeomBegin = 0
            numGeomEnd   = numGeomBegin - 1
            #No --N arg specified so we take the number of molecules in the file as --N and filename as output
            if nByBatch<1:
                N = df.shape[0]
                outputId = getFileOutName(files[numFile])
                n = 1 #reset

    numGeomEnd  += 1
    #print("++n")

print("# of saved geometries=", nSaved)
print("# nShape=", nShape)