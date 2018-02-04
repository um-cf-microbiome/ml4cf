# This script performs various regression operations
# on a dataset
#
# Import Python packages
import sys, math, os
import pandas as pd
from scipy.stats import linregress
# Import local subroutines
sys.path.insert(0, str(os.getcwd()+'/src/'))
import data
from data import edit, get, select

def column_list(reg_feat):
 for feature in reg_feat:
  reg_columns.append(column+'_slope')
  reg_columns.append(column+'_intercept')
 reg_results = pd.DataFrame(data=None,index=data.index,columns=reg_columns) 
 return(reg_column_list)

def patient(full_data,reg_columns):
# Performs patient-specific linear (longitudinal) regression
 unneeded_features = ['sample','sample_age','patient_id']
 reg_columns = 
# Create an empty array for regression results
 for patient in data.get.patient_ids(full_data):
#  for column in reg_columns:
#  if column not in unneeded_features:
   reg_columns.append(column+'_slope')
   reg_columns.append(column+'_intercept')
 reg_results = pd.DataFrame(data=None,index=data.index,columns=reg_columns)
# Iterate over patients
 for patient in unique_patients.unique_patient_id:
  patient_data = query_data.get_patient_df(data,patient)
# Iterate over all non-temporal features:
  for feature in patient_data.columns:
   if feature not in unneeded_features:
# Check data quality before performing regression
    print(patient_data[feature])
    if data_handling.good_data(patient_data[feature]):
     print("performing regression")
#  perform linear regression
     quit()
     print(linregress(patient_data.sample_age,patient_data[feature]))
    if not data_handling.good_data(patient_data[feature]):
     print('Patient '+patient+' has insufficient '+feature+' values for linear regression')
#   slope,intercept = linregress(patient_data.sample_age,patient_data[feature])[0,1]
#   reg_results[feature+'_slope'].loc[patient] = slope
#   reg_results[feature+'_intercept'].loc[patient] = intercept
#   print(reg_results[feature+'_intercept'].loc[patient])
 new_data = pd.concat([data,reg_results],axis=1)
 return(new_data)
