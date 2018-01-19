# This file contains basic data handling operations
import pandas as pd
import math

def remove_nonnumerical_data(data):
 numerical_data = pd.DataFrame(data=None,index=data.index)
 old_data = numerical_data
 for feature in data.columns:
  skip=False
  for sample in data.index:
   if type(data[feature].iloc[sample]) is not str:
    if math.isnan(data[feature].iloc[sample]): skip=True
  if not skip:
   numerical_data = pd.concat([old_data,data[feature]],axis=1)
  old_data = numerical_data
 return(numerical_data)

def good_data(feature):
# Evaluate quality of single-column dataframe
# Return logical argument
 total_good = 0
 good = [True for index in feature.index]
# Search for NaN entries
 for index in feature:
  print(index)
  if type(feature.iloc[index]) is not str:
   if math.isnan(feature.iloc[index]): good[index]=False
# Count numerical entries
 for index in good:
  if not good[index]:
   total_good = total_good + 1
# Mark the feature as good if 'total_good' >= 2 
 return(good)

def contains_nonnumerical_data(column):
# Logical: searches a column dataframe for non-numerical data
 NaN=False
 for index in column.index:
  if math.isnan(data[feature].iloc[sample]): NaN=True
 return(NaN)

def trim_data(data,features_to_keep):
# Trim dataframe to contain only 'features_to_keep'
 old_data = pd.DataFrame(data=None,index=data.index)
 final_data = pd.DataFrame(data=None)
 for want in features_to_keep.iloc[0]:
  for check in data.columns:
   if (str(want) == str(check)):
    final_data = pd.concat([old_data,data[check]],axis=1)
    old_data = final_data
 return(final_data)
