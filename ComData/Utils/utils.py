import os
import sys
import argparse

        
def getFileOutName(h5FileName):
        outFileName = os.path.basename(h5FileName)
        outFileName = os.path.splitext(outFileName)[0]
        return outFileName

def getArgumentsCom():
    #define command line arguments
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--N", type=int, default=-1,  help="Set max number of molecules to store inside a folder. if <1 (default) : number and name are the same of h5")
    parser.add_argument("--soft", type=str, default="Gaussian",  help="Select a software : Gaussian (default), ...")
    parser.add_argument("--params", type=str, default="enter string for the method", help="Params for calculation inside software")
    parser.add_argument("--h5dir", type=str, default="../tmp/h5", help="h5 directory (default ../tmp/h5)")
    parser.add_argument("--outdir", type=str, default="../tmp/out", help="output directory(default ../tmp/out)")


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