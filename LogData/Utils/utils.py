import os
import sys
import argparse

def getFileOutName(fileName):
        outFileName = os.path.basename(fileName)
        outFileName = os.path.splitext(outFileName)[0]
        return outFileName

def findLastOccurence(token, lines):
    index = -1
    for i, line in enumerate(lines):
        f = line.find(token)
        if f != -1:
            index = i
    return index

def findAllOccurence(token, lines):
    indexes = []
    for i, line in enumerate(lines):
        f = line.find(token)
        if f != -1:
            indexes.append(i)
    return indexes

def getArguments():
    #define command line arguments
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--logdir", type=str, default="../tmp/log", help=".log directory (default ../tmp/log)")
    parser.add_argument("--infile", type=str, default="default", help="previous hdf file containing specific information about the molecules. If unspecified, the columns such as SMILES or InChI will be NaN.")
    parser.add_argument("--outfile", type=str, default="../tmp/out.h5", help="output hdf file (default ../tmp/out.h5)")
    

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