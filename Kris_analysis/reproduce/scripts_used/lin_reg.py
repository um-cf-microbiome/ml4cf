# This script performs linear regression
import sys
import pandas as pandas
import os
import numpy as np
from scipy.stats import linregress
import math

data_to_keep = ['patient_id','sample_age','fev1','shannondiv','shannoneven','invsimpson','anaerobe_abundance','strict_anaerobe_abundance','oral_anaerobe_abundance']
data_file = sys.argv[1]
data = pandas.read_csv(data_file,sep=',')
data_to_fit = []
# Select features to fit with linear regression
for i in data_to_keep:
 for j in data.iloc[0,:]:
  print(i)
  print(j)
  if str(i) == str(j):
   data_to_fit.hstack([data_to_fit,data.iloc[:,j]],1)
print(data_to_fit)
quit()

for x in list(set(data['patient_id'].tolist())):
    samples = []
    for index, row in data.iterrows():
        if row['patient_id'] == x:
            samples.append([row['sample_age'],row['fev1'],row['shannondiv'],row['shannoneven'],row['invsimpson'],row['anaerobe_abundance'],row['strict_anaerobe_abundance'],row['oral_anaerobe_abundance']])
    #if x == 336:
    #    print samples    
    outs=str(x)+','

    for i in range(1,len(samples[0])):
        ys = []
        xs = []

        for s in samples:
            if not math.isnan(s[i]):
                xs.append(s[0])
                #print s[i]
                ys.append(s[i])

        if len(xs)>0:

            outs += str(linregress(xs,ys)[0]) +','+str(linregress(xs,ys)[1])+','
        else:
            outs += 'NA,NA,'
        
    print(outs)

