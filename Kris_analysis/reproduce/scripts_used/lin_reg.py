# This script performs linear regression
# on a dataset
import sys, math
import pandas as pd
import data_handling, query_data
from scipy.stats import linregress

def lin_reg_patient_specific(data):
# Group data by patient for linear (longitudinal) regression
 unique_patients = query_data.get_patient_ids(data)
 list_of_features = list(data_handling.trim_data(data,[data.columns])) 
 reg_columns = list()
 for column in list_of_features:
  reg_columns.append(column+'_slope')
  reg_columns.append(column+'_intercept')
 reg_results = pd.DataFrame(data=None,index=data.index,columns=reg_columns)
# Iterate over patients
 for patient in unique_patients.unique_patient_id:
  
  patient_data = data_handling.trim_data(query_data.get_patient_df(data,patient),query_data.get_patient_df(data,patient).columns)
# Iterate over features:
  for feature in patient_data.columns:
   if feature != 'sample_age':
# Check data quality before performing regression
    if data_handling.good_data(patient_data[feature]):
#  perform linear regression
     print(linregress(patient_data.sample_age,patient_data[feature]))
    if not data_handling.good_data(patient_data[feature]):
     print('Patient '+patient+' has insufficient '+feature+' values for linear regression')
#   slope,intercept = linregress(patient_data.sample_age,patient_data[feature])[0,1]
#   reg_results[feature+'_slope'].loc[patient] = slope
#   reg_results[feature+'_intercept'].loc[patient] = intercept
#   print(reg_results[feature+'_intercept'].loc[patient])
 new_data = pd.concat([data,reg_results],axis=1)
 return(new_data)
