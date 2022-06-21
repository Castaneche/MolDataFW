
import pandas as pd
import numpy as np
import sys

sys.path.append('Utils')
from utils import *
from PeriodicTable import *

#typical layout for n2p2 file
"""
begin
comment by xLogML : From a0.log file, All value are in AU
atom 0.000000000000 5.388582648150 0.000000000000 C -0.073760000000 0.000000000000 0.000000000000 -0.000006363000 0.000000000000
atom 0.000000000000 2.700223176744 0.000000000000 C 0.050820000000 0.000000000000 0.000000000000 0.000009271000 0.000000000000
atom 2.360941613109 6.686180616316 0.000000000000 C -0.215490000000 0.000000000000 -0.000003752000 0.000000796000 0.000000000000
energy  -921.92601237700001
charge  0.00000000000000
dipole 0.00000000000179 -0.00000000000134 0.00000000000002
end
"""

def determinePCToken(nparr, rowindex):
    s = 'Partial Charges (Hirshfeld)'
    if type(nparr[s][rowindex]) is list:
        return s
    s = 'Partial Charges (ESP)'
    if type(nparr[s][rowindex]) is list:
        return s
    s = 'Partial Charges (NPA)'
    if type(nparr[s][rowindex]) is list:
        return s
    s = 'Partial Charges (Mulliken)'
    if type(nparr[s][rowindex]) is list:
        return s
    #None of them
    return None

def convert(infile, outfile):
    try:
        pt = PeriodicTable() 
        
        f = open(outfile, "w")
        df = pd.read_hdf(infile, 'df')
        
        #convert to record array so we can access a cell easily nparr['colname'][rowindex]
        nparr = df.to_records()
        for rowindex in range(len(nparr)): #each row is a molecule
            try:
                sout = 'begin\n'
                sout += 'comment by begin conver_h5_n2p2 idx= {:2}\n'.format(rowindex)
                natoms = len(nparr['Atoms'][rowindex])

                pcToken = determinePCToken(nparr, rowindex) 

                for i in range(0,natoms): #iterate over atoms to write coords, forces and Z symbol
                    sout1 = 'atom {:20.14f} {:20.14f} {:20.14f} '.format(nparr['Coordinates'][rowindex][i*3 + 0], 
                                                             nparr['Coordinates'][rowindex][i*3 + 1],
                                                             nparr['Coordinates'][rowindex][i*3 + 2])
                    z = nparr['Atoms'][rowindex][i]
                    e = pt.elementZ(z)
                    sout2 = '{:6s}'.format(e.symbol)

                    if pcToken != None:
                            sout3 =' {:20.14} '.format(nparr[pcToken][rowindex][i])
                    else:
                            sout3 =' {:20.14} '.format(0.0)
                    sout4 =' {:20.14f} '.format(0.0)
                    sout5 ='{:20.14f} {:20.14f} {:20.14f} '.format(nparr['Forces'][rowindex][i*3 + 0],
                                                        nparr['Forces'][rowindex][i*3 + 1],
                                                        nparr['Forces'][rowindex][i*3 + 2])

                    sout += sout1 + sout2 + sout3 + sout4 + sout5 + '\n'

                sout += 'energy {:20.14f}\n'.format(nparr['Energy'][rowindex])
                sout += 'charge {:20.14f}\n'.format(nparr['Charge'][rowindex])
                sout +='dipole {:20.14f} {:20.14f} {:20.14f}\n'.format(nparr['Dipole'][rowindex][0], 
                                                                 nparr['Dipole'][rowindex][1],
                                                                 nparr['Dipole'][rowindex][2])

                sout += 'end\n'
                f.write(sout)
            	#print(sout)
            except:
                print("Error for molecule number ", rowindex)
        f.close()
    except Exception as Ex:
        print("ReadFailed")
        raise Ex
    return

args = getArguments()

convert(args.infile, args.outfile)
