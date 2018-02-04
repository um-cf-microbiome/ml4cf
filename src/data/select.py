# This file contains subroutines for data selection
# and querying of a pandas dataframe.  It is intended 
# for use with microbiome sequence analyses
import pandas as pd

def classifier(data,classifier,class_names):
# Selects subset of 'data' matching
# the value for 'class_name' in 'column'
 subset_data = pd.DataFrame(data=None,columns=data.columns)
 old_data = pd.DataFrame(data=None,columns=data.columns) 
 for feature in data.columns:
  if feature == classifier:
   for sample in data.index:
    for class_i in class_names:
     if data[feature].iloc[sample] == class_i:
      concatframe = pd.DataFrame(data=[data.iloc[sample]],index=[len(old_data[feature])+1],columns=old_data.columns)
      subset_data = pd.concat([old_data,concatframe],axis=0)
      old_data = subset_data
 return(subset_data)
