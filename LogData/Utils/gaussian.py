import pandas as pd
import numpy as np
from Utils.utils import *
from Utils.constants import *

'''
Get dataFrame for Gaussian prop with nan value
'''
def getNanGaussianDataFrame(nlines):
    data = {'cid' : [np.nan] *nlines,
           'Charge'  : [np.nan] *nlines,
           'Multiplicity' : [np.nan] *nlines , 
           'Atoms' : [np.array(np.nan)] *nlines,
           'Method' : [np.nan] *nlines ,
           'Coordinates': [np.nan] *nlines , 
           'Forces' : [np.nan] *nlines,
           'Frequencies' : [np.nan] *nlines,
           'Energy' : [np.nan] *nlines,
           'Dipole' : [np.nan] *nlines ,
           'Quadrupole' : [np.nan] *nlines,
           'Partial Charges (Mulliken)' : [np.nan] *nlines ,
           'Partial Charges (Hirshfeld)' : [np.nan] *nlines ,
           'Partial Charges (ESP)' : [np.nan] *nlines,
           'Partial Charges (NPA)' : [np.nan] *nlines
          }
    return pd.DataFrame(data)




def getXYZ(lineId, lines, columnToSkip = []):
    '''
    Return a list of coordinates following a specific pattern (see coordinates or forces below)
    '''
    arr = []
    while True:
        line = lines[lineId]
        #iterate util the end of forces
        if '-------' in line:
            break;

        numbers = line.split()
        for i, num in enumerate(numbers):
            if i in columnToSkip: #skip specified columns
                continue
            arr.append(float(num))
        lineId += 1
    return arr

def GetAtoms(lines):
    #Getting atoms and coordinates is very similar (see GetCoords() for typical layout)
    try:
        token = 'Coordinates (Angstroms)'
        lineId = findLastOccurence(token, lines)
        atoms = np.NaN #default value
        if lineId != -1:
            lineId += 3
            print('Atoms found at line : ', lineId)
            arr = []
            while True:
                line = lines[lineId]
                #iterate util the end of forces
                if '-------' in line:
                    break;

                numbers = line.split()
                for i, num in enumerate(numbers):
                    if i == 1:
                        arr.append(int(num))
                lineId += 1
            atoms = arr
        else:
            print('Error : can\'t get atom values')
            return np.NaN
    except:
        print('Error : can\'t get atom values')
        return np.NaN
    return atoms

def GetCoords(lines):
    #Typical layout for coordinates
    """
    ---------------------------------------------------------------------
    Center     Atomic      Atomic             Coordinates (Angstroms)
    Number     Number       Type             X           Y           Z
    ---------------------------------------------------------------------
    1          6           0        0.838045   -0.555170   -0.389292
    2          6           0        2.319444   -0.240344   -0.146179
    3          6           0        2.598590   -0.582209    1.300598
    ---------------------------------------------------------------------
    """
    try:
        coordsToken = 'Coordinates (Angstroms)'
        coordsLineId = findLastOccurence(coordsToken, lines)
        coords = np.NaN #default value
        if coordsLineId != -1:
            coordsLineId += 3
            print('Coordinates found at line : ', coordsLineId)
            coords = getXYZ(coordsLineId, lines, [0,1,2])
        else:
            print('Error : can\'t get coordinate values')
            return np.NaN
    except:
        print('Error : can\'t get coordinate values')
        return np.NaN
    return np.array(coords) * BOHRPERA

def GetForces(lines):
    #Typical layout for forces
    """
    -------------------------------------------------------------------
    Center     Atomic                   Forces (Hartrees/Bohr)
    Number     Number              X              Y              Z
    -------------------------------------------------------------------
    1        6          -0.000001038   -0.000000154    0.000000772
    2        6           0.000001366    0.000001994    0.000001602
    3        6          -0.000000206    0.000000264   -0.000000980
    -------------------------------------------------------------------
    """
    try:
        forcesToken = 'Forces (Hartrees/Bohr)'
        forcesLineId = findLastOccurence(forcesToken, lines)
        forces = np.NaN #default value
        if forcesLineId != -1:
            forcesLineId += 3
            print('Forces found at line : ', forcesLineId)
            forces = getXYZ(forcesLineId, lines, [0,1])
        else:
            print('Error : can\'t get force values')
            return np.NaN
    except:
        print('Error : can\'t get force values')
        return np.NaN
    return forces

def GetFrequencies(lines):
    #Typical layout for forces
    """
                        160                    161                    162
                         A                      A                      A
    Frequencies --   1604.4824              1680.1255              2865.5430
    """
    try:
        token = 'Frequencies'
        lineIds = findAllOccurence(token, lines)
        frequencies = np.NaN #default value
        if len(lineIds) > 0:
            print('Frequencies found at line : ', lineIds[0])
            arr = []
            for lineId in lineIds:
                s = lines[lineId].split()
                arr.append(float(s[2]))
                arr.append(float(s[3]))
                arr.append(float(s[4]))
            frequencies = arr
        else:
            print('Error : can\'t get frequencie values')
            return np.NaN
    except:
        print('Error : can\'t get frequencie values')
        return np.NaN
    return frequencies

def GetChargeAndSpin(lines):
    #Typical layout for spin and charge
    """
    Charge = 0 Multiplicity = 1
    """
    try:
        token = 'Charge ='
        lineId = findLastOccurence(token, lines)
        if lineId != -1:
            print('Charge and Spin found at line : ', lineId)
            s = lines[lineId].split()
            charge = int(s[2])
            multiplicity = int(s[5])
        else:
            print('Error : charge and spin not found')
    except:
        print('Error : can\'t get charge and spin values')
        return np.NaN, np.NaN
    return charge, multiplicity

def GetEnergyXTB(lines, energyLineId):
    #Retreive energy
    energyLineId += 1
    print('Energy found at line : ', energyLineId)
    try:
        energy = float(lines[energyLineId].split()[1])
    except:
        print('Error : can\'t get energy value')
        return np.NaN
    return energy

def GetDipoleXTB(lines, dipoleLineId):
    #retreive dipole
    print('Dipole found at line : ', dipoleLineId)
    try:
        dipole = [float(i) for i in lines[dipoleLineId].split()[4:]]
        if len(dipole) < 3:
            return np.NaN
    except:
        print('Error : can\'t get dipole values')
        return np.NaN
    return dipole

def GetEnergyDFT(lines, energyLineId):
    print('DFT Energy found at line : ', energyLineId)
    try:
        energy = float(lines[energyLineId].split()[4])
    except:
        print('Error : can\'t get energy value')
        return np.NaN
    return energy

def GetEnergyCCSDT(lines, energyLineId):
    print('CCSD(T) Energy found at line : ', energyLineId)
    try:
        energyStr = lines[energyLineId].split()[1]
        energyStr = energyStr.replace('D', 'E')
        energy = float(energyStr)
    except:
        print('Error : can\'t get energy value')
        return np.NaN
    return energy

def GetEnergyCCSD(lines, energyLineId):
    print('CCSD Energy found at line : ', energyLineId)
    try:
        energyStr = lines[energyLineId].split('E(Corr)=')[1]
        energy = float(energyStr)
    except:
        print('Error : can\'t get energy value')
        return np.NaN
    return energy

def GetEnergyMP2(lines, energyLineId):
    print('MP2 Energy found at line : ', energyLineId)
    try:
        energyStr = lines[energyLineId].split('EUMP2 =')[1]
        energyStr = energyStr.replace('D', 'E')
        energy = float(energyStr)
    except:
        print('Error : can\'t get energy value')
        return np.NaN
    return energy

def GetDipole(lines):
    #Typical layout for dipole
    """
    Dipole moment (field-independent basis, Debye):
    X=              0.8301    Y=              0.7032    Z=              0.8796  Tot=              1.3990
    """
    try:
        token = 'Dipole moment'
        lineId = findLastOccurence(token, lines)
        if lineId != -1:
            lineId += 1
            print('Dipole found at line : ', lineId)
            s = lines[lineId].split()
            dipole = [float(s[1]), float(s[3]), float(s[5])]
        else:
            print('Error : dipole not found')
            return np.NaN
    except:
        print('Error : can\'t get dipole values')
        return np.NaN
    return np.array(dipole) * AUPERDEBYE

def GetQuadrupole(lines):
    #Typical layout for qadrupole
    """
    Quadrupole moment (field-independent basis, Debye-Ang):
    XX=            -33.9271   YY=            -33.7195   ZZ=            -39.8202
    XY=             -0.6758   XZ=              5.1678   YZ=              5.8704
    """
    try:
        token = 'Quadrupole moment'
        lineId = findLastOccurence(token, lines)
        if lineId != -1:
            lineId += 1
            print('Quadrupole found at line : ', lineId)
            s1 = lines[lineId].split()
            s2 = lines[lineId+1].split()
            quadrupole = [float(s1[1]), float(s1[3]), float(s1[5]),
                          float(s2[1]), float(s2[3]), float(s2[5])]
        else:
            print('Error : quadrupole not found')
            return np.NaN
    except:
        print('Error : can\'t get quadrupole values')
        return np.NaN
    return np.array(quadrupole) * AUPERDEBYE * BOHRPERA

def GetMullikenCharges(lines, nbatoms):
    #Typical layout for Mulliken charges
    """
 Mulliken charges:
               1
     1  C   -0.942277
     2  C   -0.140845
    """
    try:
        token = 'Mulliken charges:'
        lineId = findLastOccurence(token, lines)
        mulliken = np.NaN
        if lineId != -1:
            lineId += 2
            print('Partial charges (Mulliken) found at line : ', lineId)
            mulliken = []
            i = 0
            while i < nbatoms:
                s = lines[lineId+i].split()
                mulliken.append(float(s[2]))
                i+=1
        else:
            print('Error : partial charges (Mulliken) not found')
            return np.NaN
    except:
        print('Error : can\'t get partial charge (Mulliken) values')
        return np.NaN
    return mulliken

def GetHirshfeldCharges(lines, nbatoms):
    #Typical layout for Mulliken charges
    """
 Hirshfeld charges, spin densities, dipoles, and CM5 charges using IRadAn=      5:
              Q-H        S-H        Dx         Dy         Dz        Q-CM5   
     1  C   -0.086305   0.000000   0.014808  -0.005423   0.010435  -0.233858
     2  C   -0.013401   0.000000  -0.001999  -0.003500  -0.017864  -0.075699
    """
    try:
        token = 'Hirshfeld charges,'
        lineId = findLastOccurence(token, lines)
        hirshfeld = np.NaN
        if lineId != -1:
            lineId += 2
            print('Partial charges (Hirshfeld) found at line : ', lineId)
            hirshfeld = []
            i = 0
            while i < nbatoms:
                s = lines[lineId+i].split()
                hirshfeld.append(float(s[7]))
                i+=1
        else:
            print('Error : partial charges (Hirshfeld) not found')
            return np.NaN
    except:
        print('Error : can\'t get partial charge (Hirshfeld) values')
        return np.NaN
    return hirshfeld

def GetESPCharges(lines, nbatoms):
    #Typical layout for Mulliken charges
    """
 ESP charges:
               1
     1  C   -0.507892
     2  C    0.345351
    """
    try:
        token = 'ESP charges:'
        lineId = findLastOccurence(token, lines)
        esp = np.NaN
        if lineId != -1:
            lineId += 2
            print('Partial charges (ESP) found at line : ', lineId)
            esp = []
            i = 0
            while i < nbatoms:
                s = lines[lineId+i].split()
                esp.append(float(s[2]))
                i+=1
        else:
            print('Error : partial charges (ESP) not found')
            return np.NaN
    except:
        print('Error : can\'t get partial charge (ESP) values')
        return np.NaN
    return esp

def GetNPACharges(lines, nbatoms):
    #Typical layout for Mulliken charges
    """
                Natural  -----------------------------------------------
    Atom  No    Charge         Core      Valence    Rydberg      Total
 -----------------------------------------------------------------------
      C    1   -0.67664      1.99950     4.66773    0.00941     6.67664
      C    2   -0.31355      1.99914     4.29724    0.01717     6.31355
      C    3   -0.44135      1.99932     4.42910    0.01293     6.44135
    """
    try:
        token = 'Natural  ----'
        lineId = findLastOccurence(token, lines)
        npa = np.NaN
        if lineId != -1:
            lineId += 3
            print('Partial charges (NPA) found at line : ', lineId)
            npa = []
            i = 0
            while i < nbatoms:
                s = lines[lineId+i].split()
                npa.append(float(s[2]))
                i+=1
        else:
            print('Error : partial charges (NPA) not found')
            return np.NaN
    except:
        print('Error : can\'t get partial charge (NPA) values')
        return np.NaN
    return npa

'''
Read all data from a gaussian log file
'''
def readGaussianLogFile(filepath):
    lines = []
    with open(filepath, 'r') as file:
        # read all lines in a list
        lines = file.readlines()

    if len(lines) == 0:
        print('Error : no data available at ', filepath)
        return pd.DataFrame() #return an empty DataFrame
    #print("Last line = ",lines[-1])
    if(lines[-1].find("Normal termination")==-1):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(" Error  : Not normal termination of Gaussian calculation")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return pd.DataFrame()
    
    energy = np.NaN #default value
    dipole = np.NaN #default value
    quadrupole = np.NaN #default value
    method = '';        
    
    #coords, forces and frequencies have similar layout for each method
    atoms = GetAtoms(lines)
    if type(atoms) is not list: #no point continuing the data won't be exploitable
        return pd.DataFrame()
    
    coords = GetCoords(lines)
    forces = GetForces(lines)
    frequencies = GetFrequencies(lines)
    charge, spin = GetChargeAndSpin(lines)
    
    
    #Huge if-else to determine which log file we have
    #Energy has different format for each method so we just look for specific energy tokens
    energyToken = ' CCSD(T)'
    energyLineId = findLastOccurence(energyToken, lines)
    if energyLineId != -1: #CCSDT log file
        method = 'CCSDT'
        energy = GetEnergyCCSDT(lines, energyLineId)
        dipole = GetDipole(lines)
        quadrupole = GetQuadrupole(lines)
    else:
        energyToken = 'amplitudes converged. E(Corr)'
        energyLineId = findLastOccurence(energyToken, lines)
        if energyLineId != -1: #CCSD log file
            method = 'CCSD'
            energy = GetEnergyCCSD(lines, energyLineId)
            dipole = GetDipole(lines)
            quadrupole = GetQuadrupole(lines)
        else:
            energyToken = 'EUMP2'
            energyLineId = findLastOccurence(energyToken, lines)
            if energyLineId != -1: #MP2 log file
                method = 'MP2'
                energy = GetEnergyMP2(lines, energyLineId)
                dipole = GetDipole(lines)
                quadrupole = GetQuadrupole(lines)
            else:
                energyToken = 'SCF Done:'
                energyLineId = findLastOccurence(energyToken, lines)
                if energyLineId != -1: #DFT log file
                    method = 'DFT';
                    energy = GetEnergyDFT(lines, energyLineId)
                    dipole = GetDipole(lines)
                    quadrupole = GetQuadrupole(lines)
                else:
                    energyToken = 'Recovered energy='
                    energyLineId = findLastOccurence(energyToken, lines)
                    if energyLineId != -1: #XTB log file
                        method = 'XTB';
                        energy = GetEnergyXTB(lines, energyLineId)
                        dipole = GetDipoleXTB(lines, energyLineId)
                        #quadrupole are not calculated with xtb
                    else:
                        print('Error : log file doesn\'t match a known method')
                        return pd.DataFrame()

    mulliken = GetMullikenCharges(lines, len(atoms))
    hirshfeld = GetHirshfeldCharges(lines, len(atoms))
    esp = GetESPCharges(lines, len(atoms))
    npa = GetNPACharges(lines, len(atoms))
    
    #Get cid because we need a way to determine which molecule it is
    cid = int(getFileOutName(filepath))
    
    #DataFrame
    #df = getNanGaussianDataFrame(1)
    row = {'cid' : cid,
           'Charge' : charge,
           'Multiplicity' : spin, 
           'Atoms': [atoms],
           'Method' : method,
           'Coordinates': [coords], 
           'Forces': [forces],
           'Frequencies' : [frequencies],
           'Energy': energy,
           'Dipole' : [dipole],
           'Quadrupole': [quadrupole],
           'Partial Charges (Mulliken)' : [mulliken],
           'Partial Charges (Hirshfeld)' : [hirshfeld],
           'Partial Charges (ESP)' : [esp],
           'Partial Charges (NPA)' : [npa],
          }
    #for key in row.keys():
         #df.loc[:,key].update(row[key])
#    print(df)
    df = pd.DataFrame(row)
    
    return df

