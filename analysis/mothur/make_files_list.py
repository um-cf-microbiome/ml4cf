# This script searches for fastq files in
# subdirectories, moves them to a common sub-folder
# called 'fastq_files' (in the current directory)
# and creates 'stability.files'

# Requires a '.csv' file with the sample 
# IDs in the first column as input, and the column name 'Sputum_Number'

import pandas, os, glob, subprocess
import os.path, platform, csv
from shutil import copyfile

def compare_file_size(file_1,file_2):
 if os.path.getsize(file_1) > os.path.getsize(file_2): result = True
 else: result = False
 return(result)
    
sample_list_file=str("/home/meek/NTM/analysis/sample_list.csv")
control_list_file=str("/home/meek/NTM/analysis/mothur/control_list.csv")
stability_files=open(str("/home/meek/NTM/analysis/mothur/stability.files"),'w')
fastq_dir=str("/home/meek/data/fastq_files/")
# Read sputum ID numbers
sample_list = pandas.read_csv(sample_list_file)['Sputum Number']
control_list = pandas.read_csv(control_list_file)['Control']
forward_read_flag = str("L001_R1_001")
reverse_read_flag = str("L001_R2_001")
written_list = list()

# Search sub-directories for fastq files with matching sputum ID
for top,sub_dirs,files in os.walk(fastq_dir):
 continue
# Loop over files
for sample in sample_list:
 if not sample in written_list:
  forward = False
  reverse = False
  for file in files:
   sample_str = str(sample+'_')
   sample_str_test1 = str(sample+'M')
   sample_str_test2 = str(sample+'O')
   sample_str_test3 = str(sample+'b')
   if (sample_str in file) or (sample_str_test1 in file) or (sample_str_test2 in file) or (sample_str_test3 in file):
    if not sample in written_list:
     if forward_read_flag in file: 
      forward_file = str(fastq_dir+file)
      forward = True
     if reverse_read_flag in file: 
      reverse_file = str(fastq_dir+file)
      reverse = True
     if reverse and forward:
      stability_files.write(sample+" "+forward_file+" "+reverse_file+"\n")
      written_list.append(sample)
    
for sample in control_list:
 if not sample in written_list:
  forward = False
  reverse = False
  for file in files:
   sample_str = str(sample+'_')
   sample_str_test1 = str(sample+'M')
   sample_str_test2 = str(sample+'O')
   sample_str_test3 = str(sample+'b')
   if (sample_str in file) or (sample_str_test1 in file) or (sample_str_test2 in file) or (sample_str_test3 in file):
    if not sample in written_list:
     if forward_read_flag in file: 
      forward_file = str(fastq_dir+file)
      forward = True
     if reverse_read_flag in file: 
      reverse_file = str(fastq_dir+file)
      reverse = True
     if reverse and forward:
      stability_files.write(sample+" "+forward_file+" "+reverse_file+"\n")
      written_list.append(sample)
    
