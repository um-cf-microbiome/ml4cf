# This script contains support vector machine (SVM) 
# analyses for the first positive NTM dataset of 
# Dr. Lindsay Caverly, University of Michigan
# Dept. of Pediatric Pulmonology
# Analyses completed in January-March, 2018.
#
# Script written by Garrett A. Meek
# 
# This file is organized as follows:
# 
# (1) Load software
#     (1-A) Import Python packages
#     (1-B) Point to non-Python software
#     (1-C) Import local Python source
# (2) Microbiome analysis with mothur
# (3) Microbiome analysis with entropart
# (4) Build dataframes
#     (4-A) Make datasets
#                   'microbial_full': Contains all default microbial
#                   data from Mothur MiSeq-SOP, where the data was subsequently
#                   used to calculate individual OTU relative abundances
#	                  'microbial_main_ntm_only': Contains microbial data for samples that
#		                tested positive for M. avium or M. abscessus only
#	                  'index_and_prior_sample_only': Contains microbial data for the sample
#                   closest to the NTM index date, as well as the most recent prior sample
#     (4-B) Augment dataset with entropart biodiversity measures
#     (4-C) Regression with RAs and biodiversity features
# (5) Train SVM models
#     (5-A) Feature selection and F-scores with 'libsvm' 
#          Format dataset for 'libsvm'

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
import datetime, socket
from os import system, unlink
from collections import defaultdict
from subprocess import *
from shutil import copyfile
import numpy as np
import pylab as pl
import sklearn
from sklearn import svm
#     (1-B) Point to non-Python software

#           'mothur' for sequencing

# machine-specific paths
if socket.gethostname() == 'WSPDR062': 
 host_base = str("F:/")
 mothur_path = str(host_base+"software/mothur/mothur.exe")
 R_path=str('C:/Program Files/R/R-3.4.3/bin/Rscript.exe')
if socket.gethostname() == 'DESKTOP-8OVG652': 
 host_base = str("D:/")
 mothur_path = str(host_base+"software/mothur_win/mothur/mothur.exe")
if socket.gethostname() == 'elbel': 
 host_base = str("/home/"+os.environ.get('USER')+"/")
 mothur_path = str(host_base+"software/mothur/")
if socket.gethostname() == 'flux-login1.arc-ts.umich.edu': 
 host_base = str("/home/"+os.environ.get('USER')+"/")
 mothur_path = str(host_base+"software/mothur/")

processors=8
run_base=str(host_base+"NTM/")
classifiers_file=open(str(host_base+'NTM/analysis/classifiers.csv'),'r')
sample_list_file=open(str(host_base+'NTM/analysis/sample_list.csv'),'r')
control_list_file_name = str(host_base+'NTM/analysis/control_sample_list.csv')
control_list_file = open(control_list_file_name,'r')
fastq_dir=str(host_base+"data/fastq_files/")
mothur_ref_dir=str(host_base+"data/fastq_files/")
stability_files_name = str(host_base+'NTM/analysis/mothur/stability.files')
stability_files=open(stability_files_name,'w')
batch_file_name = str(host_base+'NTM/analysis/mothur/stability.batch')
batch_file=open(batch_file_name,'w')
mothur_output_path=str(host_base+"NTM/analysis/mothur/")
sys.path.insert(0,str(host_base+'software/libsvm/tools'))
sys.path.insert(0,str(host_base+"NTM/src"))
#     (1-C) Import local Python source

#           'libsvm' for SVM analysis
#           (https://github.com/cjlin1/libsvm)
#           grid.py finds best combo. of C/gamma for SVM training
import grid

import data, model
from data import edit, get, select
from eco import mothur#, entropart
from model import regression
#           'csv2libsvm.py' to convert csv file to libsvm format
#           (https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py)
from data import csv2libsvm
#           'fselect.py' calculates F-scores and CV% accuracy
#           (https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/#feature_selection_tool)
from model import fselect

# (2) Microbiome analysis with Mothur

# Use samples in 'Sputum Number' column to make .files
sample_list = pd.read_csv(sample_list_file)['Sputum_Number']
# Add samples included in 'Control' column of control_list_file
control_list = pd.read_csv(control_list_file)['Sputum_Number']
# Make mothur stability.files from sample and control lists
mothur.make_stability_files(sample_list,control_list,stability_files,fastq_dir)
# Make mothur batch file:
mothur.make_batch(stability_files_name,batch_file,mothur_ref_dir,control_list,mothur_output_path,processors)
# Run mothur SOP:
mothur.run(mothur.cmd_line(mothur_path,batch_file_name,mothur_output_path))
# Unfinished steps to calculate Shannon Beta using 'entropart' (R)
# https://github.com/EricMarcon/entropart

#entropart.run()
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
