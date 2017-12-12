import sys
import pandas as pandas
import os
from scipy.stats import linregress
import math

#long_fix.py > long_features.csv

data = pandas.read_csv('cav_dataset_subset.csv')



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
        
    print outs

