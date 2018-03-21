# This script performs analyses 
# for the first positive culture NTM cohort of 
# Dr. Lindsay Caverly, University of Michigan
# Dept. of Pediatric Pulmonology
#
# Analyses completed in January-March, 2018.
#
# Script written by Garrett A. Meek with help from
# Kris Opron (python source) and Madsen Zimbric (data)
# 

# (1) Load software

#     (1-A) Import Python packages

import pandas as pd
import random, subprocess, shutil, collections
import sys, os, csv, platform, fnmatch
import datetime, socket
from os import system, unlink
from collections import defaultdict
from subprocess import *
from shutil import copyfile
import numpy as np
import pylab as pl
import sklearn
from sklearn import svm
#           (https://github.com/cjlin1/libsvm)
#           grid.py finds best combo. of C/gamma for SVM training
import grid
import data, model, classes
from data import edit, get, select, clean
from eco import mothur#, entropart
from classes import job, host
from model import regression

job_name = 'ntm'
# Initialize the 'job.info' class, which defines global variables for the job
job_info = job.info(job_name=str(job_name),host_info=host.info())
# Use samples in 'Sputum Number' column to make .files
job_info.sample_list = pd.read_csv(job_info.sample_list_file)['Sputum_Number']
# Add samples included in 'Control' column of control_list_file
job_info.control_list = pd.read_csv(job_info.control_list_file)['Sputum_Number']

# Remove output files from previous run
#clean.old_files(job_info)

#           'csv2libsvm.py' to convert csv file to libsvm format
#           (https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py)
#from data import csv2libsvm
#           'fselect.py' calculates F-scores and CV% accuracy
#           (https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/#feature_selection_tool)
#from model import fselect

# (2) Microbiome analysis with Mothur

# Make mothur stability.files from sample and control lists
mothur.make_stability_files(job_info)
# Make and run mothur SOP batch file:
mothur.batch(job_info)

# Calculate Shannon Beta using 'entropart' (R)
# https://github.com/EricMarcon/entropart
entropart.batch(job_info)

# (3) Build dataframes
#     (3-A) Read data and build dataframes

#data_file = open(str(os.getcwd()+'NTM/data/ntm-first-positive-incomplete.csv'),'r')
#clinical_feat_file = open(str(os.getcwd()+'NTM/analysis/clinical_features.csv'),'r')
#reg_feat_file = open(str(os.getcwd()+'NTM/analysis/regression_features.csv'),'r')
#classifiers_file = open(str(os.getcwd()+'NTM/analysis/classifiers.csv'),'r')    

# Construct pandas dataframes
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
#      regression_results = lin_reg.lin_reg_patient(regression_input)
# (4) Train SVM model
#     (4-A) Format dataset for 'libsvm'
#     (4-B) Train SVM models with the following variations:
#            i) Each classifier (Disease yes/no, transient/persistent, MAC/Mab.)
#min_C,max_C,step_C = -2,9,2
#C_range = str(min_C+','+max_C+','+step_C)
#min_gamma,max_gamma,step_gamma = 1,-11,-2
#gamma_range = str(min_gamma+','+max_gamma+','+step_gamma)
#grid_exe_input = str('-log2c '+C_range+' -log2g '+gamma_range)
#            iii) Vary F-score threshold
#            iv) Vary SVM-included features (above F-score threshold)
# (6) Plot results
#
