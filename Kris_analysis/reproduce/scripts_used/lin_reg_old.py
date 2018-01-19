# This script performs linear regression
# on a dataset
import sys, math
import pandas as pd
import data_handling
from scipy.stats import linregress

def lin_reg_func(data):
 lin_reg_data_file = 'lin_reg.out'
# Group the data by patient for linear (longitudinal) regression
 for sample1 in data.index:
  output = []
  sample_age = []
  feature_value = []
  for sample2 in data.index:
   if data['patient_id'].iloc[sample1] == data['patient_id'].iloc[sample2] and sample1 != sample2:
    for column in data.columns:
# Check for non-numerical data
     if column != 'sample' and not math.isnan(data[column].iloc[sample1]):
       sample_age.append(data['sample_age'].iloc[sample2])
       feature_value.append(data[column].iloc[sample2])
  if len(sample_age)>0:
   output += str(linregress(sample_age,feature_value)[0]) +','+str(linregress(sample_age,feature_value)[1])+','
  else:
   output += 'NA,NA,'
  print(sample_age)
  print(feature_value)
 print(output)
 return(output)
