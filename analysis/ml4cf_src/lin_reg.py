# This script performs linear regression
# on a dataset
#
# Import Python packages
import sys, math, os
import pandas as pd
from scipy.stats import linregress
# Import local subroutines
sys.path.insert(0, str(os.getcwd()+'/analysis/ml4cf_src'))
import data_handling
import query_data

def lin_reg_patient(data):
# Group data by patient for linear (longitudinal) regression
 unneeded_features = ['sample','sample_age','patient_id']
 unique_patients = query_data.get_patient_ids(data)
 
 list_of_features = list(data_handling.trim_data(data,data.columns)) 
 reg_columns = list()
# Create an empty array for regression results
 for feature in list_of_features:
  if feature not in unneeded_features:
   reg_columns.append(feature+'_slope')
   reg_columns.append(feature+'_intercept')
 reg_results = pd.DataFrame(data=None,index=data.index,columns=reg_columns)
# Iterate over patients
 for patient in unique_patients.unique_patient_id:
  patient_data = query_data.get_patient_df(data,patient)
# Iterate over all non-temporal features:
  for feature in patient_data.columns:
   if feature not in unneeded_features:
# Check for data before performing regression
    if data_handling.good_data(patient_data[feature]):
# Replace NaN with feature average
     patient_data[feature] = data_handling.replace_nan_with_avg(patient_data[feature])
#  Perform linear regression
     reg = linregress(patient_data.sample_age,patient_data[feature])
#  Store results
     reg_results[feature+'_slope'].loc[patient] = reg[0]
     reg_results[feature+'_intercept'].loc[patient] = reg[1]
    if not data_handling.good_data(patient_data[feature]):
#     print('Patient ',patient,' has insufficient '+feature+'data for linear regression')
     reg_results[feature+'_slope'].loc[patient] = 'None'
     reg_results[feature+'_intercept'].loc[patient] = 'None'
 new_data = pd.concat([data,reg_results],axis=1)
 print(new_data.iloc[0])
 quit()
 return(new_data)
