import numpy as np
import pandas as pd
import random
import os
import sys
import argparse

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

def getArguments():
    #define command line arguments
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--infile", type=str, default="", help="h5 file")
    parser.add_argument("--infileG", type=str, default="", help="h5 file with G functions")
    parser.add_argument("--outfile", type=str, default="", help="output file")
    

    #if no command line arguments are present, config file is parsed
    config_file='config.txt'
    fromFile=False
    if len(sys.argv) == 1:
        fromFile=True
    if len(sys.argv) == 2 and sys.argv[1].find('--') == -1:
        config_file=sys.argv[1]
        fromFile=True

    if fromFile is True:
        print("Try to read configuration from ",config_file, "file")
        if os.path.isfile(config_file):
            args = parser.parse_args(["@"+config_file])
        else:
            args = parser.parse_args(["--help"])
    else:
        args = parser.parse_args()
        
    return args

args = getArguments()

sample = []

Atoms = [1,6,7,8]
for Z in Atoms:
    df = pd.read_hdf(args.infileG,'Z' + str(Z))

    k = 50
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(df)

    df["predicted_cluster"] = kmeans.labels_

    percentage = 0.22

    for i in range(k):
        indexes = df.index[df['predicted_cluster'] == i].tolist()
        indexes = list(set(indexes))
        n = max( [int( len(indexes) * (percentage/100.0) ), 1])
        sample.extend(random.sample(indexes, n))

    
    
print(len(sample))
sample = set(sample)
print(len(sample))


database = pd.read_hdf(args.infile, 'df')
out = database.loc[sorted(sample)]
print(len(out))
out.to_hdf(args.outfile, 'df')
