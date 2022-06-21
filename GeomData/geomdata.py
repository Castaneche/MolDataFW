'''
Loop through each tar file inside a directory and read json data files to extract interesting values
Fill and save a dataframe to hdf file
'''

import time
import sys
import os
import pandas as pd
import numpy as np
import glob
import shutil
import tarfile

from Utils.utils import *
from Utils.constants import *

#these are the parameters (ordered) that we want to find inside the json files
#a dot means we go deep in the dictionary : see getInDict function in Utils/utils.py
#the values are the final output name and type in the database
parameters = {'Isomeric SMILES': ('Isomeric SMILES', object),
              'InChI': ('InChI', object),
              'cid': ('cid', float),
              'molecular formula': ('molecular formula', object),
              'charge': ('charge', float),
              'multiplicity': ('multiplicity', float),
              'PM6.atoms.elements.number': ('atoms', object),
              'PM6.atoms.coords.3d': ('coords', object),
              'PM6.properties.energy.total': ('energy (PM6)', float)
             }

#Read a molecule json data file
#'arr' is the two dimensional numpy array (see below : moldata)
#'k' is the row index of the current data corresponding to a single molecule
def readMolFile(pathToJsonFile, arr, k):
    #read json data
    data = pd.read_json(pathToJsonFile)
    data = data['pubchem'] #get series
    
    #loop through each parameters listed above and retreive the values
    for i, keyInJson in enumerate(parameters.keys()):
        arr[k][i] = getInDict(data, keyInJson)
    arr[k]['coords'] = np.array(arr[k]['coords']) * BOHRPERA
    return arr


#Get arguments
argv = sys.argv
source = argv[1]
tarFile = os.path.basename(source)
storageDir=os.path.dirname(source)

tar = tarfile.open(source)
njsons=0
for member in tar.getmembers():
    if ".json" in member.name:
        njsons = njsons + 1

print("njsons=",njsons)
#create a 2D numpy array as a temporary database (because numpy is faster than pandas)
moldata = np.empty(shape=[njsons], dtype=list(parameters.values()))

#loop through each json file inside tar file
i=-1
for member in tar.getmembers():
    if ".json" in member.name:
        i=i+1
        print("name=",member.name)
        file=tar.extractfile(member)
        moldata = readMolFile(file, moldata, i)

tar.close()

#create a DataFrame based on extracted data
df = pd.DataFrame(moldata)
#Save as hdf5 
fileName = os.path.basename(source).split(".")[0]
print(fileName)
df.to_hdf(os.path.join(storageDir, fileName + ".h5"), 'df')

