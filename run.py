# This script contains the protocol
# for support vector machine (SVM) analysis of
# the first positive NTM dataset of Dr. Lindsay Caverly.
# University of Michigan, Dept. of Pediatric Pulmonology
# January, 2018.
#
# Authors: Lindsay Caverly, Garrett Meek
# 
# This file is organized as follows:
# 
# (1) Load software
#     (1-A) Load Python packages
#     (1-B) Load/point to non-Python software
#     (1-C) Load local subroutines
# (2) Microbiome analysis with Mothur
# (2) Build dataframes
#     (2-A) Read data and build dataframes for ML
#           (2-A-i) Build microbial datasets:
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
#	            'microbial_avium': Contains microbial data for samples that
#		    tested positive for M. avium
#	            'microbial_abscessus': Contains microbial data for samples that
#		    tested positive for M. abscessus
#           (2-A-ii) Build clinical datasets:
#	            'clinical_full': Contains all clinical features (described in:
#	            'data/features_description.txt')
#	            'clinical_numeric': Contains only the clinical features
#		    whose values are numeric
#                   'clinical_no_fev1': Contains all clinical features except 'fev1'
# (3) Add derived features
#     (2-B) Add subject-specific regression results as features
# (4) Train SVM model to classify NTM disease
#     (A) 
# (5) Prepare analysis results for plotting
# (6) Plot results

##
#
# (1) Load Python packages and read datasets
#
##
# (1) Load software
#     (1-A) Load Python packages
import pandas as pd
import sys, os, csv, platform
from collections import defaultdict
from subprocess import call
#     (1-B) Load/point to non-Python software

#     (1-C) Load local subroutines
sys.path.insert(0, str(os.getcwd()+'/src'))
import data, model
from data import edit, get, select
from model import regression
# (2) Microbiome analysis with Mothur

#     (1-B) Read data and build dataframes for ML

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
