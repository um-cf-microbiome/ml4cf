# This script contains support vector machine (SVM) 
# analyses for the first positive NTM dataset of 
# Dr. Lindsay Caverly, University of Michigan
# Dept. of Pediatric Pulmonology
# Analyses completed in January-February, 2018.
#
# Script written by Garrett A. Meek
# 
# This file is organized as follows:
# 
# (1) Load software
#     (1-A) Import Python packages
#     (1-B) Point to non-Python software
#     (1-C) Import local Python source
# (2) Microbiome analysis with Mothur
# (3) Build dataframes
#     (3-A) Read data and build dataframes
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
#	                  'microbial_avium': Contains microbial data for samples that
#		                tested positive for M. avium
#	                  'microbial_abscessus': Contains microbial data for samples that
#		                tested positive for M. abscessus
#	                  'clinical_full': Contains all clinical features (described in:
#	                  'data/features_description.txt')
#	                  'clinical_numeric': Contains only the clinical features
#		                whose values are numeric
#                   'clinical_no_fev1': Contains all clinical features except 'fev1'
#     (3-B) Append subject-specific regression results as features in dataframe
# (4) Train SVM model
#     (4-A) Format dataset for 'libsvm'
#     (4-B) Train SVM models with the following variations:
#            i) Vary classifiers (Disease yes/no, transient/persistent, MAC/Mab.)
#            ii) Vary F-score threshold
#            iii) Vary SVM-included features (above F-score threshold)
# (6) Plot results

##
#
#  BEGIN ANALYSIS
#
##


# (1) Load software

#     (1-A) Import Python packages

import pandas as pd
import random, subprocess, shutil, collections
import sys, os, csv, platform, fnmatch
import datetime
from os import system, unlink
from collections import defaultdict
from subprocess import *
from shutil import copyfile

#     (1-B) Point to non-Python software

#           'mothur' for sequencing

#if platform.system() == 'Windows':
mothur_path = str("F:\\software\\mothur\\mothur.exe")
sample_list_file=open('F:\\NTM\\analysis\\sample_list.csv','r')
control_list_file = open('F:\\NTM\\analysis\\control_sample_list.csv','r')
fastq_dir=str("F:\\data\\fastq_files")
mothur_ref_dir=str("F:\\analysis\\mothur\\ref\\")
stability_files=open('F:\\NTM\\analysis\\mothur\\stability.files','w')
batch_file=open('F:\\NTM\\analysis\\mothur\\stability.batch','w')
mothur_output_file=str("F:\\NTM\\analysis\\mothur\\mothur.out")
#if platform.system() == 'Linux':
# sample_list_file=str(os.getcwd()+"sample_list.csv")
# stability_files=str(os.getcwd()+"stability.files")
# fastq_search_dir=str('F:/data/NTM/fastq_files/')
# fastq_folder=str(os.getcwd()+"fastq_files")

#     (1-C) Import local Python source

#           'libsvm' for SVM analysis

#           (https://github.com/cjlin1/libsvm)
sys.path.insert(0, str('F:\\software\\libsvm-3.22\\tools'))
#           grid.py finds best combo. of C/gamma for SVM training
import grid

sys.path.insert(0, str('F:\\NTM\\src'))
import data, model, reverse_read, mothur
from data import edit, get, select
from model import regression
#           'csv2libsvm.py' to convert csv file to libsvm format
#           (https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py)
#           'fselect.py' calculates F-scores and CV% accuracy
#           (https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/#feature_selection_tool)
from data import csv2libsvm
from model import fselect

# (2) Microbiome analysis with Mothur

# Use samples in 'Sputum Number' column to make .files
sample_list = pandas.read_csv(sample_list_file)['Sputum Number']
# Add samples included in 'Control' column of control_list_file
control_list = pandas.read_csv(control_list_file)['Control']
# Make stability.files
mothur.make_stability_files(sample_list,control_list,stability_files,fastq_dir)
# Make mothur batch file:
mothur.make_batch(stability_files,batch_file,mothur_ref_dir,control_list)
# Run mothur SOP:
mothur_command = str(mothur_path+' '+batch_file+' > 'mothur_output_file)
mothur.run(mothur_command)


# (3) Build dataframes
#     (3-A) Read data and build dataframes
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
#	                  'microbial_avium': Contains microbial data for samples that
#		                tested positive for M. avium
#	                  'microbial_abscessus': Contains microbial data for samples that
#		                tested positive for M. abscessus
#	                  'clinical_full': Contains all clinical features (described in:
#	                  'data/features_description.txt')
#	                  'clinical_numeric': Contains only the clinical features
#		                whose values are numeric
#                   'clinical_no_fev1': Contains all clinical features except 'fev1'
#     (3-B) Append subject-specific regression results as features in dataframe
# (4) Train SVM model
#     (4-A) Format dataset for 'libsvm'
#     (4-B) Train SVM models with the following variations:
#            i) Each classifier (Disease yes/no, transient/persistent, MAC/Mab.)
min_C,max_C,step_C = -2,9,2
C_range = str(min_C+','+max_C+','+step_C)
min_gamma,max_gamma,step_gamma = 1,-11,-2
gamma_range = str(min_gamma+','+max_gamma+','+step_gamma)
grid_exe_input = str('-log2c '+C_range+' -log2g '+gamma_range)
#            iii) Vary F-score threshold
#            iv) Vary SVM-included features (above F-score threshold)
# (6) Plot results
#

#     (2-A) Build Mothur input files
if platform.system() == 'Windows':
 sample_list_file=open('F:\\NTM\\analysis\\sample_list.csv','r')
 control_list_file = open('F:\\NTM\\analysis\\control_sample_list.csv','r')
 stability_files=open('F:\\NTM\\analysis\\mothur\\stability.files','w')
 fastq_dir=str("F:\\data\\fastq_files")
 mothur_output_file=str("F:\\NTM\\analysis\\mothur\\mothur.out")
 mothur_path = str("F:\\software\\mothur\\mothur.exe")


#          Make stability.files
sample_list = pd.read_csv(sample_list_file).Sputum_Number             
control_list = pd.read_csv(control_list_file).Sputum_Number
# Get fastq files with matching sputum IDs
for top,sub_dirs,files in os.walk(fastq_dir):
 continue
# Search 'fastq_dir' for fastq files
for sample in sample_list:
 for file in files:
  if str(sample+"_") in file and str("_"+sample) not in file:
   if str("R1") in file: forward_read_file = os.path.join(fastq_dir,file)
   if str("R2") in file: reverse_read_file = os.path.join(fastq_dir,file)
 stability_files.write(sample+" "+os.path.join(fastq_dir,forward_read_file)+" "+os.path.join(fastq_dir,reverse_read_file)+"\n")
# Read in control list (Forward read controls only)
for control in control_list:
 sample = control.split('_L001',1)[0]
 forward_read_file = os.path.join(fastq_dir,control)
 reverse_read_file = reverse_read.find(sample,files) 
 stability_files.write(sample+" "+os.path.join(fastq_dir,forward_read_file)+" "+os.path.join(fastq_dir,reverse_read_file)+"\n")
quit()

#        Run mothur
#call_syntax = str(mothur_path+" "+stability_files+" > "+mothur_output_file)
#subprocess.call(call_syntax,shell=True)

# (3) Build dataframes
#     (3-A) Read data and build dataframes for ML
# Detect OS
if platform.system() == 'Linux':
    #           Linux-formatted path to data files (CSV-format)
 data_file = open(str(os.getcwd()+'/data/ntm-first-positive-incomplete.csv'),'r')
# 	    List of clinical features
 clinical_feat_file = open(str(os.getcwd()+'/analysis/clinical_features.csv'),'r')
#           List of regression features
 reg_feat_file = open(str(os.getcwd()+'/analysis/regression_features.csv'),'r')
#	    List of classifiers
 classifiers_file = open(str(os.getcwd()+'/analysis/classifiers.csv'),'r')
#           Read files
if platform.system() == 'Windows':
    #  Windows-formatted path to data files
 data_file = open(str(os.getcwd()+'NTM\\data\\ntm-first-positive-incomplete.csv'),'r')
 clinical_feat_file = open(str(os.getcwd()+'NTM\\analysis\\clinical_features.csv'),'r')
 reg_feat_file = open(str(os.getcwd()+'NTM\\analysis\\regression_features.csv'),'r')
 classifiers_file = open(str(os.getcwd()+'NTM\\analysis\\classifiers.csv'),'r')    

# Construct pandas dataframes
full_data = pd.read_csv(data_file)
clinical_features = clinical_feat_file.read().splitlines()
reg_feat = reg_feat_file.read().splitlines()
classifiers = classifiers_file.read().splitlines()
#	    Determine microbial features by removing clinical features
microbial_features = data.edit.remove(full_data,clinical_features).columns
#           (1-B-i) Define microbial datasets:
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
microbial_full = data.edit.keep(full_data,microbial_features)
print(microbial_full.columns)
quit()
#
#		    Assemble data for samples with M. avium and M. abscessus only
microbial_avium_absc = data.select.classifier(full_data,'ntm_species',['M. avium complex','M. abscessus complex'])
#		    Assemble individual datasets for each microbial classifier:

#                   'microbial_avium': Contains microbial data for samples with M. avium
microbial_avium = data.select.classifier(full_data,'ntm_species',['M. avium complex'])
#                   'microbial_abscessus': Contains microbial data for samples with M. acscessus
microbial_absc = data.select.classifier(full_data,'ntm_species',['M. abscessus complex'])
#           (1-B-ii) Define clinical datasets:
#                   'clinical_full': Contains all clinical features (described in:
#                   'data/features_description.txt')
clinical_full = data.edit.keep(full_data,clinical_features)
#                   'clinical_numeric': Contains only the clinical features
#                   whose values are numeric
clinical_numeric = data.edit.keep_numeric(clinical_full)
#                   'clinical_no_fev1': Contains all clinical features except 'fev1'
clinical_no_fev1 = data.edit.remove(clinical_full,['fev1','index_fev1','baseline_fev1'])

# (2) Add derived features to dataset
#     (2-A) Calculate standard diversity measures
#     (2-B) Perform subject-specific regression

clinical_supp_data = model.regression.patient(clinical_full)
print(clinical_supp_data.columns)
quit()
microbial_supp_data = model.regression.patient(microbial_full)
print(clinical_supp_data.columns)
print(microbial_supp_data.columns)
# 'model_data' contains all features used for F-score and SVM analysis
model_data = pd.concat([full_data,supp_data],axis=1)
quit()

##
#
# (3) Define SVM training datasets
#
##

# Assemble training datasets to answer questions of interest:

## (A) Which features predict NTM disease classification (large F-score) for the cohort?

## (B) Which features predict NTM disease classification for individual patients?

#
# 'data': complete dataset (including regression results)
data = regression_results
# 'pair_data'*: paired NTM/non-NTM disease samples for each patient (possessing both)
# * for patients with more than one NTM/non-NTM sample the feature value is calculated as the average

# (3) 
# (4) 

##
#
# (4) Train SVM model to classify NTM disease
#
##

#lib_svm = svm.csv_to_libsvm(regression_results)

# Convert CSV data-file to SVM library

# Perform SVM analysis with LIBSVM

#y.get_patient_df(data,patient) 

##
#
# (4) Get NTM-disease prediction F-score for all features
#
##

# Calculate F-score for all features

##
#
# (5) Plot results
#
##

# Plot regression results

# Plot F scores for all features

#      regression_results = lin_reg.lin_reg_patient(regression_input)
