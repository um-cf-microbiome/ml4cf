# This script performs various regression operations
# on a dataset
#
# Import Python packages
import sys, math, os
import pandas as pd
from scipy.stats import linregress
# Import local subroutines
os.chdir('../../')
sys.path.insert(0, str(os.getcwd()+'/src/'))
import data
from data import edit, get, select

def column_list(reg_feat):
 reg_columns = list()
 for feature in reg_feat:
  reg_columns.append(feature+'_slope')
  reg_columns.append(feature+'_intercept')
 return(reg_columns)

def patient(full_data):
# Performs patient-specific linear (longitudinal) regression
 numeric_data = data.edit.keep_numeric(full_data)
 reg_columns = numeric_data.columns
 unneeded_features = ['sample','sample_age','patient_id','relative_age','index_age']
# Create empty array for regression results
 reg_results = pd.DataFrame(data=None,index=full_data.index,columns=reg_columns)
 for patient in data.get.patient_ids(full_data):
  patient_data = data.edit.keep_numeric(data.get.patient_df(full_data,patient))
# Iterate over non-temporal features:
  for feature in patient_data.columns:
   if feature not in unneeded_features:
# Check data for errors
    x_data = pd.DataFrame(data=None,index=None,columns=['relative_age'])
    y_data = pd.DataFrame(data=None,index=None,columns=[feature])
    for row in patient_data.index:
     time = patient_data['relative_age'].iloc[row-1]
     y = patient_data[feature].iloc[row-1]
     if math.isfinite(time) and math.isfinite(y):
      concatframe_x = pd.DataFrame(data=[time],index=[len(x_data.index)],columns=['relative_age'])
      concatframe_y = pd.DataFrame(data=y,index=[len(y_data.index)],columns=[feature])
      x_data = pd.concat([x_data,concatframe_x],axis=0)
      y_data = pd.concat([y_data,concatframe_y],axis=0)
    slope,intercept,rvalue,pvalue,stderr = linregress(x_data['relative_age'],y_data[feature])
    print(rvalue,pvalue,stderr)
    quit()
    reg_results[feature+'_slope'].loc[patient] = slope
    reg_results[feature+'_intercept'].loc[patient] = intercept
    print(rvalue,pvalue,stderr)
 return(reg_results)
