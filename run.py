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
fastq_dir=str("F:\\data\\fastq_files\\")
mothur_ref_dir=str("F:\\analysis\\mothur\\ref\\")
stability_files=open('F:\\NTM\\analysis\\mothur\\stability.files','w')
stability_files_name = 'F:\\NTM\\analysis\\mothur\\stability.files'
batch_file=open('F:\\NTM\\analysis\\mothur\\stability.batch','w')
batch_file_path= 'F:\\NTM\\analysis\\mothur\\stability.batch'
mothur_output_file=str("F:\\NTM\\analysis\\mothur\\mothur.out")
#if platform.system() == 'Linux':
# sample_list_file=str(os.getcwd()+"sample_list.csv")
# stability_files=str(os.getcwd()+"stability.files")
# fastq_search_dir=str('F:/data/NTM/fastq_files/')
# fastq_folder=str(os.getcwd()+"fastq_files")

#     (1-C) Import local Python source

#           'libsvm' for SVM analysis

#           (https://github.com/cjlin1/libsvm)
sys.path.insert(0, str('F:\\software\\libsvm\\tools'))
#           grid.py finds best combo. of C/gamma for SVM training
import grid

sys.path.insert(0, str('F:\\NTM\\src'))
import data, model, reverse_read
from data import edit, get, select, mothur
from model import regression
#           'csv2libsvm.py' to convert csv file to libsvm format
#           (https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py)
#           'fselect.py' calculates F-scores and CV% accuracy
#           (https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/#feature_selection_tool)
from data import csv2libsvm
from model import fselect

# (2) Microbiome analysis with Mothur

# Use samples in 'Sputum Number' column to make .files
sample_list = pd.read_csv(sample_list_file)['Sputum_Number']
# Add samples included in 'Control' column of control_list_file
control_list = pd.read_csv(control_list_file)['Sputum_Number']
# Make stability.files
mothur.make_stability_files(sample_list,control_list,stability_files,fastq_dir)
# Make mothur batch file:
mothur.make_batch(stability_files_name,batch_file,mothur_ref_dir,control_list)
# Run mothur SOP:
mothur.run(mothur.cmd_line(mothur_path,batch_file_path,mothur_output_file))


# (3) Build dataframes
#     (3-A) Read data and build dataframes

#data_file = open(str(os.getcwd()+'NTM\\data\\ntm-first-positive-incomplete.csv'),'r')
#clinical_feat_file = open(str(os.getcwd()+'NTM\\analysis\\clinical_features.csv'),'r')
#reg_feat_file = open(str(os.getcwd()+'NTM\\analysis\\regression_features.csv'),'r')
#classifiers_file = open(str(os.getcwd()+'NTM\\analysis\\classifiers.csv'),'r')    

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