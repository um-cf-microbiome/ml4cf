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
 good = pd.DataFrame(data=True,index=feature.index,columns=['good_data'])
# Search for NaN entries
 for index in feature.index:
  if type(feature.iloc[index-1]) is str:
   if math.isnan(feature.iloc[index-1]): good['good_data'].iloc[index-1]=False 
  if str(feature.iloc[index-1]) == 'nan': good['good_data'].iloc[index-1]=False
# Count numerical entries
 for index in good.index:
  if good['good_data'].iloc[index-1]:
   total_good = total_good + 1
# Mark the feature as good if 'total_good' >= 2 
 if total_good >= 2:
  good_set = True
 else:
  good_set = False
 return(good_set)

def replace_nan_with_avg(feature):
# Replace NaN entries with the feature average
 entries = 0
 total = 0.0
# Get the sum
 for index in feature.index:
  if str(feature.iloc[index-1]) != 'nan':
   feature_total = sum([float(total),float(feature.iloc[index-1])])
   entries = entries + 1
   total = feature_total
# Calculate average
 avg = total / entries
# Replace NaN with avg
 new_feature = feature
 for index in feature.index:
  if str(feature.iloc[index-1]) == 'nan':
   feature.iloc[index-1] = avg
 print(new_feature)
 return(new_feature) 

def replace_nan_with_reg_values(feature,sample_age,slope):
# Replace NaN entries with feature regression values
 return(new_feature)

def check_for_nan(column):
# Logical: searches a column dataframe for non-numerical data
 NaN=False
 for index in column.index:
  if math.isnan(column.iloc[index-1]): NaN=True
 return(NaN)

def trim_data(data,features_to_keep):
# Trim dataframe to contain only 'features_to_keep'
 old_data = pd.DataFrame(data=None,index=data.index)
 final_data = pd.DataFrame(data=None)
 for want in features_to_keep:
  for check in data.columns:
   if (want == check):
    final_data = pd.concat([old_data,data[check]],axis=1)
    old_data = final_data
 return(final_data)
