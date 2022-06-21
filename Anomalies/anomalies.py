'''
This program eliminates molecules with wrong energy value
It scans the database using a clustering algorithm to identify outliers and remove them.
'''

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from numpy import where
from sklearn.preprocessing import StandardScaler, MaxAbsScaler, MinMaxScaler, RobustScaler
from Utils.utils import * #getArguments()

def dbscan_outlier_prediction(X, epsilon=1, min_samples=10, **kwargs):
    '''
    Use dbscan to find clusters, then identify and return a list of outliers 
    '''
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, **kwargs)
    dbscan.fit(X)
    pred = dbscan.fit_predict(X)
    mol_index_outlier = where(pred == -1)
    label_counts = [(i, np.sum(dbscan.labels_==i)) for i in set(dbscan.labels_)]
    label_counts.sort(key=lambda x : -x[1]) # sort by counts per class, descending
    return mol_index_outlier,label_counts, dbscan.labels_


def removeOutlier(df):
    '''
    Use dbscan_outlier_prediction to identify outliers and remove them from the dataframe
    '''
    numLines=np.arange(df.shape[0])    
    fl=pd.DataFrame(df['Energy'])
    fl['NumLines']=numLines
    X = StandardScaler().fit_transform(fl)
    eps=1
    min_sample=10
    mol_index_outlier, label_counts, labels = dbscan_outlier_prediction(X, epsilon=eps, min_samples=min_sample)
    df.drop(df.index[mol_index_outlier], axis=0, inplace=True)
    return df, len(mol_index_outlier[0])

args = getArguments()

df = pd.read_hdf(args.infile, 'df')

# for testing
df.loc[17081.0, 'Energy'] = 10000
df.loc[24989.0, 'Energy'] = 1000
df.loc[16.0, 'Energy'] = 5
df.loc[15.0, 'Energy'] = 100

#Loop to get all diverging values, 
#the database is reduced each time so smaller diverging values are identifiable at the next iteration

lo = 1
while lo > 0:
    print(df[df['Energy']>0]['Energy'])
    df,lo=removeOutlier(df)
    print("lo=",lo)

print("Final Results")
print(df[df['Energy']>0]['Energy'])

df.to_hdf(args.outfile, 'df')



