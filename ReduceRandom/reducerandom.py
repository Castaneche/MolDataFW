import pandas as pd
import glob
import random
import os
import sys
import argparse

def getArguments():
    #define command line arguments
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--infile", type=str, default="", help="input file (.h5)")
    parser.add_argument("--outfile", type=str, default="", help="output file (.h5)")
    parser.add_argument("--percent", type=int, default=10, help="amount of database to keep (default to 10%)")

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

percentage = args.percent

df = pd.read_hdf(args.infile, 'df')
print(df.shape)

n = int(len(list(df.index)) * percentage/100.0)
indexes = random.sample(list(df.index), n)
df = df[df.index.isin(indexes)]
df.to_hdf(args.outfile, 'df')