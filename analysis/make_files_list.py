#!/usr/bin/env python
# This python script searches for fastq files in
# subdirectories, moves them to a common sub-folder
# called 'fastq_files' in the current directory
# and creates 'stability.files'

# The script requires a '.csv' file with the sample 
# IDs in the first column as input

import pandas, os
import os.path, platform

if platform.system() == 'Windows':
 sample_list_file=str(os.getcwd()+"\\sample_list.csv")
 stability_files=str(os.getcwd()+"\\stability.files")
 fastq_search_dir=str('F:\\data\\NTM\\fastq_files\\')
 fastq_folder=str(os.getcwd()+"\\fastq_files")
if platform.system() == 'Linux':
 sample_list_file=str(os.getcwd()+"sample_list.csv")
 stability_files=str(os.getcwd()+"stability.files")
 fastq_search_dir=str('F:/data/NTM/fastq_files/')
 fastq_folder=str(os.getcwd()+"fastq_files")

if not os.path.exists(fastq_folder): os.mkdir(fastq_folder)
print(sample_list_file)
files_list=pandas.read_csv(sample_list_file,delim_whitespace=True,header=None)                     
#print(files_list)
#for root, dirs, files in os.walk(fastq_folder)
#    for file in files:
#        print (file)
        
#
#write_file=open(new_list_file,"w")
#for i in range(0,len(files_list.iloc[:,0])):
# print(files_list.iloc[i,1])
# print(files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0])
# files_list.iloc[i,0]=files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0]
#files_list.to_csv(write_file,sep=' ',index=False,header=None)
