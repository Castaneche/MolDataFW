# MolDataFW
Multiple scripts to manage a large molecule database. We provide scripts to extract molecular data from the PubChem database, generate input files for Gaussian software and reading Gaussian output files. This is done during a 6 weeks internship at Institut Lumière Matière (ILM). 

# Structure
## GeomData
This script extracts interesting data from PubChem database and store the result inside a hdf file. 

## ComData
This script read previous hdf file and generates a .com file readable by Gaussian software. Computation are performed using Gaussian and this typically outputs a .log file we can read later.

## LogData
This script read the .log file outputed by Gaussian and tries to retreive some interesting values such as energy, forces...

## ConvertData
This folder contains some script to convert hdf file to other types. It is used when performing machine learning algorithms on data.

## wACSF
It contains scripts used to compute G functions for each atoms. The G function describes the surroundings of an atom and is used later to perform a selection over molecules.

## Clustering
The scripts inside this folders perform a clustering algorithm using G functions. This way, we can exclude molecule that are similar and therefore not necessary to keep.

## ReduceRandom
Contains a script to take a sample of molecule randomly inside the database. 

## Metrics
This folder contains helpers to analyse the database. It outputs histogram for particular properties of molecules and perform some comparison between databases.


# Credits
This work was done under supervision of [ALLOUCHE Abdul Rahman](https://ilm.univ-lyon1.fr/index.php?option=com_directory&task=profile&id=34)
