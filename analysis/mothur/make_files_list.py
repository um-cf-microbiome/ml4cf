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
 sample_list_file=str("F:\\NTM\\analysis\\sample_list.csv")
 stability_files=str("F:\\NTM\\analysis\\mothur\\stability.files")
 fastq_search_dir=str("F:\\data\\fastq_files")
 fastq_folder=str("F:\\NTM\\analysis\\mothur\\fastq_files")
if platform.system() == 'Linux':
 sample_list_file=str(os.getcwd()+"sample_list.csv")
 stability_files=str(os.getcwd()+"stability.files")
 fastq_search_dir=str('F:/data/NTM/fastq_files/')
 fastq_folder=str(os.getcwd()+"fastq_files")
# Read sputum ID numbers
if not os.path.exists(fastq_folder): os.mkdir(fastq_folder)
sample_list = pandas.read_csv(sample_list_file).Sputum_Number             

# Search sub-directories for fastq files with matching sputum ID
for top,sub_dirs,files in os.walk(fastq_search_dir):
 continue
# Loop over files
for file in files:
 if not os.path.isfile(os.path.join(fastq_folder,file)) or not compare_file_size(os.path.join(fastq_search_dir,file),os.path.join(fastq_folder,file)): 
  for sample in sample_list:
   sample_str = str(sample+"_")
   if sample_str not in os.path.join(fastq_folder,file):
    if sample_str in file and not str("_"+sample+" ") in file:
     copyfile(os.path.join(top,file),os.path.join(fastq_folder,file))

        #     print(os.path.join(directory,file_name))
#     print(os.path.join(fastq_folder,file_name))
#     os.rename(os.path.join(directory,file_name),os.path.join(fastq_folder,file_name))
#     mv_cmd = str("mv "+os.path(file_name)+" "+fastq_folder)
#    print(mv_cmd)
#    if platform.system() == 'Windows': 
#     for slash in mv_cmd: str.replace('\','\\'):
#    print(mv_cmd)
#    subprocess.call(mv_cmd,shell=True)
#
#write_file=open(new_list_file,"w")
#for i in range(0,len(files_list.iloc[:,0])):
# print(files_list.iloc[i,1])
# print(files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0])
# files_list.iloc[i,0]=files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0]
#files_list.to_csv(write_file,sep=' ',index=False,header=None)
