# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 11:35:58 2016

@author: trexleraj
"""

##make name_table, which combines the descriptive names of PUMAs with PUMA id used here.
name_table=pd.read_table(r'C:\Users\trexleraj\Desktop\python dev\2010_PUMA_Names.txt',delimiter=',')
def f2(st,p):
    return str(int(st)) + '_' + str(int(p))
    
name_table.index=[f2(st,p) for st,p in zip(name_table['STATEFP'].values,name_table['PUMA5CE'].values)]

ed_key=['none','nursery','kinder','grade 1','grade 2','grade 3','grade 4','grade 5','grade 6','grade 7','grade 8','grade 9','grade 10','grade 11','grade 12','HS diploma','GED','some college','more college','assoc degree','bachelor degree','master degree','prof degree','doctorate']

def dd_on_single(single,name):
    a=defaultdict(int)
    for x in single[name]:
        a[x]+=1
    return [a]   

    
#####combined function to fetch everything faster.    
def get_summ_stats(c):
    retvals=pd.DataFrame(index=[c],columns=['name','avg','age','num','income','race','occu','cow','edu','wkw'],dtype=object)
    single=data.loc[data['rPUMA']==c]
    retvals['name']=name_table['PUMA NAME'].loc[c]
    retvals['income']=[(np.mean(single['PINCP'].loc[single['rPUMA']==c]),np.std(single['PINCP'].loc[single['rPUMA']==c]))]
    retvals['num']=pums_nums[c]
    
#    d=defaultdict(int)
#    for x in single['RAC1P']:
#        d[x]+=1
    e=defaultdict(int)
    for y in single['SOCP']:
        if y != -1:        
            e[y]+=1
    f=defaultdict(int)
    for z in single['COW']:
        if z != -1:
            f[z]+=1  
    g=defaultdict(int)
    for xx in single['SCHL']:
        if xx != -1:
            g[xx]+=1
    
    retvals['race']=dd_on_single(single,'RAC1P')
    retvals['occu']=dd_on_single(single,'SOCP')
    retvals['cow']=dd_on_single(single,'COW')
    retvals['edu']=dd_on_single(single,'SCHL')
    retvals['wkw']=dd_on_single(single,'WKW')
    retvals['age']=[(np.mean(single['AGEP'].loc[single['rPUMA']==c]),np.std(single['AGEP'].loc[single['rPUMA']==c]))] 
    return retvals
    
##write summary generating function for everything below.

 
start=time.clock()

summary=pd.DataFrame(columns=['name','avg','age','num','income','race','occu','cow','edu','wkw'],dtype=object)

#iterate over indices for whatever group of PUMAs to be analyzed.
for x in rd4_topbottom.index:
    summary=summary.append(get_summ_stats(x)) 
   

summary['avg']=rd4_topbottom['avg']
stop=time.clock()
print stop-start


### now let's plot stuff
def t1(x):
    return x[1]
def t0(x):
    return x[0]  
    
def div_ratio(x):
    s=float(np.sum(x.values()))
    m=float(np.max(x.values()))
    return (s/m)-1
    
def how_much_work(x,dwork):
    s=float(np.sum(x.values()))
    w=[]
    for entry in x:
        if entry in dwork:
            w.append(x[entry])
    return np.sum(w)/s

        
#list comprehend to get data from tuple
ages=[t0(x) for x in summary['age']]  
age_err=[t1(x) for x in summary['age']]

incomes=[t0(x) for x in summary['income']] 
income_err=[t1(x) for x in summary['income']]

race_diver=[div_ratio(x) for x in summary['race']]
race_id=[max(x,key=x.get) for x in summary['race']]

occu_diver=[div_ratio(x) for x in summary['occu']]
occu_id=[max(x,key=x.get) for x in summary['occu']]

occu_high=defaultdict(int)
for x in occu_id[:100]:
    occu_high[x]+=1
    
occu_low=defaultdict(int)
for x in occu_id[100:]:
    occu_low[x]+=1    

cow_diver=[div_ratio(x) for x in summary['cow']]
cow_id=[max(x,key=x.get) for x in summary['cow']]
cow_kids=[x[-1] for x in summary['cow']]

muchwork=[how_much_work(x,[1,2,3,4]) for x in summary['wkw']]

mat=pd.DataFrame(index=summary.index,columns=['num','avg','age','income','race diver','occu diver','occu id','cow diver','cow id','wkw','college+','fin_hs','kids'])
mat['num']=summary['num']
mat['avg']=summary['avg']
mat['age']=ages
mat['income']=incomes
mat['race diver']=race_diver
mat['occu diver']=occu_diver
mat['occu id']=occu_id
mat['cow diver']=cow_diver
mat['cow id']=cow_id
mat['wkw']=muchwork
mat['college+']=np.sum(edu_summary.iloc[:,20:24],1)
mat['fin_hs']=np.sum(edu_summary.iloc[:,15:24],1)
mat['kids']=cow_kids

natl_age=np.mean(data['AGEP'])
natl_income=np.mean(data['PINCP'])

edu_summary=pd.DataFrame(index=summary.index,columns=ed_key)

for x,idx in zip(summary['edu'],np.arange(0,len(summary))):
    for y in x.keys():
        s=float(np.sum(x.values()))
        edu_summary.iloc[idx,int(y-1)]=float(x[y]/s)