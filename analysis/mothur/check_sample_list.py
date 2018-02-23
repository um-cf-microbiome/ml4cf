# This script searches for fastq files in
# subdirectories, moves them to a common sub-folder
# called 'fastq_files' (in the current directory)
# and creates 'stability.files'

# Requires a '.csv' file with the sample 
# IDs in the first column as input

import pandas, os, glob, subprocess
import os.path, platform
from shutil import copyfile

def compare_file_size(file_1,file_2):
 if os.path.getsize(file_1) > os.path.getsize(file_2): result = True
 else: result = False
 return(result)
    
if platform.system() == 'Windows':
 sample_list_file=str("F:\\Subject-05\\mothur\\sample_list.csv")
 stability_files=str("F:\\Subject-05\\mothur\\stability.files")
 fastq_dir=str("F:\\data\\Subject-05\\fastq_files")
 missing_files=open('F:\\data\\Subject-05\\fastq_files\\missing_files.csv','w')
if platform.system() == 'Linux':
 sample_list_file=str(os.getcwd()+"sample_list.csv")
 stability_files=str(os.getcwd()+"stability.files")
 fastq_dir=str('F:/data/NTM/fastq_files/')
# Read sputum ID numbers
if not os.path.exists(fastq_dir): os.mkdir(fastq_dir)
sample_list = pandas.read_csv(sample_list_file).Sample_ID            

# Search sub-directories for fastq files with matching sputum ID
for top,sub_dirs,files in os.walk(fastq_dir):
 continue
#print(files)
# Loop over files
for sample in sample_list:
 missing=True
 for file in files:
#  print(sample,file)
  if sample in file:
   missing=False
 if missing: missing_files.write(sample+"\n")
#files_list.to_csv(write_file,sep=' ',index=False,header=None)