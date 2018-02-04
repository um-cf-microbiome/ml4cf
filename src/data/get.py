# This file contains subroutines for data selection
# and querying of a pandas dataframe.  It is intended 
# for use with microbiome sequence analyses
import pandas as pd

def counts(data):
# Get the OTU counts from a pandas dataframe
 counts = data_handling.trim_data(data,get_otu_ids(data))
 return(counts)

def total_otus(data):
# Get total number of OTUs for a sample(s)
 total = len(get_otu_ids(data))
 return(total)

def total_counts(data):
# Get total counts for each OTU in a sample(s)
 counts = data_handling.trim_data(data,get_otu_ids(data))
 total = counts.sum(axis=1)
 return(total)

def otu_ids(data):
# Get the OTU names and return them as pandas df
 otus = [col for col in data.columns if 'Otu' in col]
 if 'numOtus' in otus: otus.remove('numOtus')
 return(otus)

def patient_ids(data):
# Get unique patient IDs and return as list
 patient_ids = list()
 for index in data.index:
  if all(data.patient_id.iloc[index] != patient for patient in patient_ids):
   patient_ids.append(data.patient_id.iloc[index])
 return(patient_ids)

def patient_df(data,patient):
# Get a patient-specific dataframe
 patient_data = pd.DataFrame(data=None,columns=data.columns)
 old_patient_data = pd.DataFrame(data=None,columns=data.columns)
 for index in data.index:
  if data.patient_id.iloc[index] == patient:
   concatframe = pd.DataFrame(data=[data.iloc[index]],index=[len(old_patient_data['sample_age'])+1],columns=old_patient_data.columns)
   patient_data = pd.concat([old_patient_data,concatframe],axis=0)
   old_patient_data = patient_data
 return(patient_data)
