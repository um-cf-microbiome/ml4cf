# This file contains basic data handling operations
import pandas as pd
import numpy, math

def keep_numeric(full_data):
# Remove non-numeric columns from dataframe
 numerical_data = pd.DataFrame(data=None,index=full_data.index)
 old_data = numerical_data
 for feature in full_data.columns:
  if isinstance(full_data[feature].iloc[0],numpy.float64):
   numerical_data = pd.concat([old_data,full_data[feature]],axis=1)
   old_data = numerical_data
 return(numerical_data)

def good_data(feature):
# Evaluate quality of single-column dataframe
# Return logical argument
 total_good = 0
 good = pd.DataFrame(data=True,index=feature.index,columns=['good_data'])
# Search for NaN entries
 for index in feature.index:
  if type(feature.iloc[index-1]) is str:
   if math.isnan(feature.iloc[index-1]): good['good_data'].iloc[index]=False 
#   if good[index] == 'NaN': good[index]=False
# Count numerical entries
 for index in good.index:
  if not good.iloc[index]:
   total_good = total_good + 1
# Mark the feature as good if 'total_good' >= 2 
 print(good)
 quit()
 return(good)

def contains_nonnumerical_data(column):
# Logical: searches a column dataframe for non-numerical data
 NaN=False
 for index in column.index:
  if math.isnan(data[feature].iloc[sample]): NaN=True
 return(NaN)

def keep(data,features_to_keep):
# Trim dataframe to contain only 'features_to_keep'
 old_data = pd.DataFrame(data=None,index=data.index)
 final_data = pd.DataFrame(data=None)
 for want in features_to_keep:
  for check in data.columns:
   if (want == check or 'patient_id'):
    final_data = pd.concat([old_data,data[check]],axis=1)
    old_data = final_data
 return(final_data)

def remove(data,features_to_remove):
# Given pandas df 'data', remove columns in list 'features_to_remove'
 old_data = pd.DataFrame(data=None,index=data.index)
 final_data = pd.DataFrame(data=None)
 for feature in data.columns:
  if all(feature != remove for remove in features_to_remove):
   final_data = pd.concat([old_data,data[feature]],axis=1)
   old_data = final_data
 return(final_data)
