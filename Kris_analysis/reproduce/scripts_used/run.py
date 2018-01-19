# This script contains the protocol used
# for support vector machine (SVM) analysis of
# the first positive Caverly NTM dataset.
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
import csv
from collections import defaultdict
# Import local subroutines
import data_handling, query_data, lin_reg
# Provide path to data
data_file = '/mnt/d/NTM/data/ntm-first-positive-dataset-full.csv'
# Provide file with features for regression
regression_features_file = 'regression_features.csv'
# Read data
data = pd.read_csv(data_file)
# Read features for regression
features_for_regression = pd.read_csv(regression_features_file)
regression_input = data_handling.trim_data(data,features_for_regression)

##
#
# (2) Add subject-specific regression results as features
#
##

# regression_results contains slope and intercept data for features listed in 'regression_features_file'
regression_results = lin_reg.lin_reg_patient_specific(regression_input)
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


