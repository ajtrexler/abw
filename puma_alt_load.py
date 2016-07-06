# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 14:12:36 2016

@author: trexleraj
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter
from collections import defaultdict
from sklearn import preprocessing as ppp
from joblib import Parallel, delayed
import time
from sklearn.decomposition import PCA
import seaborn as sea
import random
import itertools
from joblib import Parallel, delayed, load, dump
import tempfile
import shutil
from sklearn import svm



filename=r'ss13pusa.csv'
filename2=r'ss13pusb.csv'
datadir=r'C:\Users\trexleraj\Desktop\python dev\comm_data'

filelist=[]
filelist=sorted(os.listdir(datadir))
data=pd.DataFrame()

#get the data.  load a defined amount from both csv files in a defined chunksize.
def get_data(datadir,total,chunk):
    data=pd.DataFrame()
    
    for f in filelist:
        name=os.path.join(datadir,f)
        toread=open(name,'r')
        chunks=pd.read_csv(toread,header=None,dtype='object',chunksize=chunk)
        df=chunks.get_chunk(size=total)
        data=pd.concat([data,df],ignore_index=True)
    
    data.columns=list(data.loc[0,:])
    del df    
    return data,name


def sparsity(x,cut):
    sparse_list=[] 
    drop_list=[]
    #code to drop features if they contain less than a given fraction of nonzero values. 
#    for rows in x:
#        if np.sum(x.loc[:,rows].values) < cut*len(x.loc[:,rows]):
#            x=x.drop(rows,axis=1)
#            drop_list.append(rows)
#    print 'dropped', len(drop_list), 'features because less than', cut*100, '% samples had nonzero values'
    for rows in x:
       
        if len(x.loc[:,rows].unique()) < 5:
            sparse_list.append(rows)
        elif (rows != 'PUMA') & (rows != 'SOCP') & (rows != 'ST') & (rows != 'rPUMA'):
            x.loc[:,rows]=ppp.scale(x.loc[:,rows].values)
    return x
               


start=time.clock()

[data,filename]=get_data(datadir,100000000,10000)

stop=time.clock()
print 'time to load:', (stop-start)/60



#drop row 0 because it has the column names imported into it.  note that this reindexes the whole business.
#drop rep_weights from end and save as separate dataframe.
data=data.drop([0])
rep_weights=data.iloc[:,203:283]
data=data.drop(rep_weights,axis=1)

data=data.convert_objects(convert_numeric=True)
data=data.fillna(-1)

def f(st,p):
    return str(int(st)) + '_' + str(int(p))

stp=[f(st,p) for st,p in zip(data['ST'].values,data['PUMA'].values)]   
rpums=pd.Series(data=stp,index=data.index)
data.loc[:,'rPUMA']=rpums 


#drop these features for various reasons but mostly because they encode stuff I don't want to anlyze.
data_ft=data.drop(['RT','SERIALNO','ADJINC'],axis=1)
#call sparsity to get back data where features with more than 5 values are scaled.  PUMA not scaled.
data_ft=sparsity(data_ft,0.5)
#build a shortdata dataframe for easy inspection anmd debugging.
shortdata=data_ft[1500:1700]



   
#get a list of all the PUMAs.
pumlist=[]
for pums in data_ft.rPUMA.values:
    if pums not in pumlist:
        pumlist.append(pums)
        
#drop occupations and rPUMA and PUMA values from data for PCA transformation.
data_ft=data_ft.drop(['PUMA'],axis=1)
pca_data=data_ft.drop(['rPUMA','SOCP'],axis=1)
#perform the PCA on puma-label-less data.
pca=PCA(n_components=20,whiten=True).fit(pca_data)
exvar=pca.explained_variance_ratio_
comps=pca.components_

#transform the full dataset with PCA.
data_transform=pd.DataFrame(pca.transform(pca_data))
data_transform['rPUMA']=pd.DataFrame(data_ft['rPUMA'].values)
data_transform['SOCP']=pd.DataFrame(data_ft['SOCP'].values)
data_ws=data_transform

#get number of samples per PUMA
pums_nums=defaultdict(int)
pums=list(data_ws.rPUMA.values)
for i in pums:
    pums_nums[i]+=1

#apply an arbitrary cutoff to make select_pums list  
pumlist2=[]
for rows in pums_nums:
    if pums_nums[rows]>10:
        pumlist2.append(rows)          

stop2=time.clock()
print 'time for total:', (stop2-start)/60



 


    
   






