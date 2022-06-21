import os
import sys
import numpy as np
import argparse

sys.path.append('Utils')
from PeriodicTable import *

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
def getArguments():
	#define command line arguments
	parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
	parser.add_argument('--infile', default='', type=str, help='')
	parser.add_argument('--outfile', default='', type=str, help='') 	
	parser.add_argument('--conv_distance', default=1.0, type=float, help="convert coefficient of distance")
	parser.add_argument('--conv_energy', default=1.0, type=float, help="convert coefficient of energy")
	parser.add_argument('--conv_dipole', default=1.0, type=float, help="convert coefficient of dipole")

	#if no command line arguments are present, config file is parsed
	config_file='config.txt'
	fromFile=False
	if len(sys.argv) == 1:
		fromFile=False
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

def convert(path, outfile, convDistance=1.0, convEnergy=1.0, convDipole=1.0):
	print("convDistance=", convDistance)
	print("convEnergy=", convEnergy)
	print("convDipole=", convDipole)
	try:
		f=open(path,"r")
		dictionary={}
		dictionary['N']=[]
		dictionary['Q']=[]
		dictionary['E']=[]
		dictionary['D']=[]
		dictionary['R']=[]
		dictionary['F']=[]
		dictionary['Qa']=[]
		dictionary['Z']=[]
		pt = PeriodicTable()
		natoms=0
		numMol = 0;
		nmaxatoms=0
		for line in f.readlines():
			if line.find('end')!= -1:
				dictionary['N'].append(natoms)
				if nmaxatoms<natoms:
					nmaxatoms=natoms
				natoms = 0
				numMol += 1
				R *= convDistance
				F *= convEnergy/convDistance
				dictionary['R'].append(R)
				dictionary['F'].append(F)
				dictionary['Qa'].append(Qa)
				dictionary['Z'].append(Z)
			elif line.find('atom') != -1:
				ll = line.split()
				if natoms==0:
					R= np.empty((0,3), float)
					Qa= []
					Z=[]
					F= np.empty((0,3), float)
				R=np.append(R, np.array([[float(ll[1]),float(ll[2]),float(ll[3])]]), axis=0)
				F=np.append(F, np.array([[float(ll[7]),float(ll[8]),float(ll[9])]]), axis=0)
				Qa = Qa + [float(ll[5])]
				#Z=np.append(Z,pt.element(ll[4]).atomicNumber)
				Z= Z + [pt.element(ll[4]).atomicNumber]
				natoms += 1

			elif line.find('charge') != -1:
				ll = line.split()
				dictionary['Q'].append(float(ll[1]))
			elif line.find('energy') != -1:
				ll = line.split()
				dictionary['E'].append(float(ll[1])*convEnergy)
			elif line.find('dipole') != -1:
				ll = line.split()
				D=np.array([float(ll[1]), float(ll[2]),float(ll[3])])
				D *= convDipole
				dictionary['D'].append(D)

		print(Z)
		print(Qa)
		for idx in range(0,numMol):
			nres=nmaxatoms-dictionary['N'][idx]
			if nres>0:
				dictionary['Z'][idx]=dictionary['Z'][idx]+[0]*nres
				dictionary['Qa'][idx]=dictionary['Qa'][idx]+[0.0]*nres
				linesR= dictionary['R'][idx]
				linesF= dictionary['F'][idx]
				for i in range(0,nres):
					linesR=np.append(linesR, np.array([[0.0,0.0,0.0]]), axis=0)
					linesF=np.append(linesF, np.array([[0.0,0.0,0.0]]), axis=0)
				dictionary['R'][idx] = linesR
				dictionary['F'][idx] = linesF
				
		#print(dictionary['N'])
		#np.savez(outfile, N=dictionary['N'], Q=dictionary['Q'], E=dictionary['E'], D=dictionary['D'], R=dictionary['R'], F=dictionary['F'], Qa=dictionary['Qa'], Z=dictionary['Z'])
		np.savez(outfile, N=dictionary['N'], Q=dictionary['Q'], E=dictionary['E'], D=dictionary['D'], F=dictionary['F'], R=dictionary['R'], Qa=dictionary['Qa'], Z=dictionary['Z'])
		f.close()
	except Exception as Ex:
		print("Read Failed.", Ex)
		raise Ex
	return

def printVect(dictionary, key, idx):
	natoms=-1
	if 'N' in dictionary: 
		natoms = dictionary['N'][idx]
	if key in dictionary: 
		print(key,":",dictionary[key][idx])
	else:
		print(key,": None")

def readnpz(filename):
        #read in data
	dictionary = np.load(filename)
        #number of atoms
	idx = len(dictionary['N'])-1

	print("idx=",idx)
	printVect(dictionary, 'N', idx)
	printVect(dictionary, 'Q',idx)
	printVect(dictionary, 'E', idx)
	printVect(dictionary, 'N', idx)
	printVect(dictionary, 'D', idx)
	printVect(dictionary, 'R', idx)
	printVect(dictionary, 'F', idx)
	printVect(dictionary, 'Qa', idx)
	printVect(dictionary, 'Z', idx)
	return

args = getArguments()
npzfile=args.outfile 
n2p2file=args.infile 
#n2p2file="a.data" 
convert(n2p2file, npzfile, convDistance=args.conv_distance, convEnergy=args.conv_energy, convDipole=args.conv_dipole)
readnpz(npzfile)
#convert("input.data")

