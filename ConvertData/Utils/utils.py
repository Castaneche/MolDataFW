import os
import sys
import argparse

def getFileOutName(h5FileName):
        outFileName = os.path.basename(h5FileName)
        outFileName = os.path.splitext(outFileName)[0]
        return outFileName

def getArguments():
    #define command line arguments
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--infile", type=str, default="", help="input file (.h5)")
    parser.add_argument("--outfile", type=str, default="", help="output file (.data)")

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