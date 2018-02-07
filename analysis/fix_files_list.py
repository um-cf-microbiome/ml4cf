#!/usr/bin/env python
# This python script modifies the format of
# stability.files so that the correct sample
# names are provided in the first column.

import pandas, os
# Provide path to list of files for Mothur

path_to_fastq=os.getcwd
files_list_file="/mnt/d/NTM/data/Castner_sequences/stability.files"
new_list_file=files_list_file+".new"
files_list=pandas.read_csv(files_list_file, delim_whitespace=True,header=None)
write_file=open(new_list_file,"w")
for i in range(0,len(files_list.iloc[:,0])):
 print(files_list.iloc[i,1])
 print(files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0])
 files_list.iloc[i,0]=files_list.iloc[i,1].split(path_to_fastq)[1].split('_')[0]
files_list.to_csv(write_file,sep=' ',index=False,header=None)
quit()
