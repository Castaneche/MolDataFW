import numpy as np
import pandas as pd
import glob
from Utils.utils import *
    
args = getArguments()

energy = []
dipole = []
dipoleX = []
dipoleY = []
dipoleZ = []
forceX = []
forceY = []
forceZ = []
data1 = {}
data2 = {}

print('Directory : ' + args.indir)
print('Compute histogram for energies : ', args.energy)
print('Compute histogram for dipoles : ', args.dipole)
print('Compute histogram for forces : ', args.force)

files = glob.glob(args.indir + '*.h5')
for f in files:
    df = pd.read_hdf(f, 'df')
    
    lens = df.loc[:, 'Dipole'].apply(lambda x: len(x) <= 2)
    df = df.drop(df[lens].index)
    
    print(df.shape)
    
    #Energy
    if args.energy == True:
        energy.extend(df.loc[:, 'Energy'])
        data1['Energy'] = energy

    #Dipole
    if args.dipole == True:
        d = np.array(df.loc[:, 'Dipole'].values.tolist())
        dipole.extend(df.loc[:, 'Dipole'])
        dipoleX.extend(d[:,0])
        dipoleY.extend(d[:,1])
        dipoleZ.extend(d[:,2])
        for i in range(len(dipole)):
            dipole[i] = np.linalg.norm(dipole[i])
        data1['DipoleNorm'] = dipole
        data1['DipoleX'] = dipoleX
        data1['DipoleY'] = dipoleY
        data1['DipoleZ'] = dipoleZ
    
    #Force
    if args.force == True:
        for index, row in df.iterrows():
            F = np.array(row['Forces'])
            forceX.extend(F[::3])
            forceY.extend(F[1::3])
            forceZ.extend(F[2::3])
        data2['ForceX'] = forceX
        data2['ForceY'] = forceY
        data2['ForceZ'] = forceZ

df = pd.DataFrame(data1)
df.to_csv(args.outfile + 'E.csv')
df = pd.DataFrame(data2)
df.to_csv(args.outfile + 'F.csv')
