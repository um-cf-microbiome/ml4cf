# This script contains the protocol used
# for support vector machine (SVM) analysis of
# the first positive NTM dataset of Dr. Lindsay Caverly..
# The basic structure of this file is shown below:
# 
# (1) Read and process data
# (2) Add subject-specific regression results as features
# (3) Train SVM model to classify NTM disease
# (4) Get NTM-disease prediction F-score for all features
# (5) Plot results

##
#
# (1) Read and process data
#
##

# Import Python packages
import pandas as pd
import sys, os, csv
from collections import defaultdict
# Import local subroutines (from ML4CF)
sys.path.insert(0, str(os.getcwd()+'/analysis/ml4cf_src'))
import data_handling, query_data, lin_reg
# Path to data file (CSV-format)
data_file = str(os.getcwd()+'/data/ntm-first-positive-dataset-full.csv')
# Path to file with list of features for regression
reg_feat_file = open(str(os.getcwd()+'/analysis/regression_features.csv'),'r')
# Read data
data = pd.read_csv(data_file)
# Read regression features
reg_feat = reg_feat_file.read().splitlines()
regression_input = data_handling.trim_data(data,reg_feat)

## Done reading user input files and processing data

##
#
# (2) Add subject-specific regression results as features
#
##

# regression_results contains slope and intercept data for features listed in 'regression_features_file'
regression_results = lin_reg.lin_reg_patient(regression_input)
#print(regression_results.iloc[1])
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

lib_svm = svm.csv_to_libsvm(regression_results)

# Convert CSV data-file to SVM library

# Perform SVM analysis with LIBSVM

y.get_patient_df(data,patient) 

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


