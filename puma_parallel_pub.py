# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 11:50:42 2016

@author: trexleraj
"""

import pandas as pd
import shapefile as sf
import csv
import matplotlib.pyplot as plt
import sklearn.cluster as skclust
import numpy as np
import os
from collections import Counter
from collections import defaultdict
from sklearn import preprocessing as ppp
from sklearn import svm
from joblib import Parallel, delayed, load, dump
import tempfile
import shutil
import time



def test_puma(pred_pum,p,score_map_mem):
    trainer=data_sub_ws.loc[data_sub_ws.rPUMA==pred_pum]
    trainer_labels=trainer.SOCP
    trainer=trainer.drop(['SOCP'],axis=1)
    trainer=trainer.drop(['rPUMA'],axis=1)
    svc=svm.SVC(kernel='linear',max_iter=10000,verbose=True).fit(trainer,trainer_labels)


    for pums2 in p:
        if pums2!=pred_pum:
            otherdata=data_ws.loc[data_ws.rPUMA==pums2]
            other_labels=otherdata.SOCP
            otherdata=otherdata.drop(['SOCP','rPUMA'],axis=1)
            score2=svc.score(otherdata,other_labels)
            score_map_mem[p_pumas.index(pred_pum),p.index(pums2)]=score2
        else:       
            score1=svc.score(trainer,trainer_labels)
            score_map_mem[p_pumas.index(pred_pum),p.index(pums2)]=score1

subpuma=list(np.random.choice(pumlist2,size=100))
start=time.clock()

#index: trainer PUMA; columns: score on that PUMA prediction.  identity will be 
#score of puma on its own training data.
score_map=pd.DataFrame(columns=subpuma, index=p_pumas)
    
tempfolder=tempfile.mkdtemp()
score_loc=os.path.join(tempfolder,'scores')
score_map_mem=np.memmap(score_loc,mode='w+',shape=np.shape(score_map),dtype=float)


if __name__== '__main__':
    Parallel(n_jobs=24, verbose=25, backend='threading')(delayed(test_puma)(t,subpuma,score_map_mem) for t in p_pumas)

rd4_score=pd.DataFrame(data=score_map_mem,index=p_pumas, columns=subpuma)

rd4_score.to_excel('160626_rd4_levelpumas.xlsx')    


     
stop=time.clock()
print (stop-start)/60