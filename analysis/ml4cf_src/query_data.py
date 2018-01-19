# This file contains subroutines for basic querying of
# a pandas dataframe, and is intended for use with
# microbiome sequence analyses
import pandas as pd
import data_handling

def get_counts(data):
# Get the OTU counts from a pandas dataframe
 counts = data_handling.trim_data(data,get_otu_ids(data))
 return(counts)

def get_total_otus(data):
# Get total number of OTUs for a sample(s)
 total = len(get_otu_ids(data))
 return(total)

def get_total_counts(data):
# Get total counts for each OTU in a sample(s)
 counts = data_handling.trim_data(data,get_otu_ids(data))
 total = counts.sum(axis=1)
 return(total)

def get_otu_ids(data):
# Get the OTU names and return them as pandas df
 otus = [col for col in data.columns if 'Otu' in col]
 if 'numOtus' in otus: otus.remove('numOtus')
 return(otus)

def get_patient_ids(data):
# Get unique patient IDs and return as pandas df
 patient_ids = pd.DataFrame(data=None,columns=['unique_patient_id'])
 old_patient_ids = patient_ids
 for index in data.index:
  stored=False
  for patient in patient_ids['unique_patient_id']:
   if patient == data.patient_id.iloc[index]: 
    stored=True
    break
  if not stored: 
   print(data)
   quit()
   current_patient = data.patient_id.iloc[index]
   concatframe = pd.DataFrame(data=[current_patient],index=[len(old_patient_ids)+1],columns=patient_ids.columns)
#   print(concatframe)
   patient_ids = pd.concat([old_patient_ids,concatframe],axis=0)
   old_patient_ids = patient_ids
 return(patient_ids)

def get_patient_df(data,patient):
 patient_data = pd.DataFrame(data=None,columns=data.columns)
 old_patient_data = pd.DataFrame(data=None,columns=data.columns)
 for index in data.index:
  if data.patient_id.iloc[index] == patient:
   concatframe = pd.DataFrame(data=[data.iloc[index]],index=[len(old_patient_data['sample_age'])+1],columns=old_patient_data.columns)
   patient_data = pd.concat([old_patient_data,concatframe],axis=0)
   old_patient_data = patient_data
 return(patient_data)
