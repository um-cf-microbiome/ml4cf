# This script contains microbiome analyses
# for Subject-05, a subject within the retrospective CF
# cohort study of Dr. John LiPuma.
#
# Written by Garrett A. Meek
# January-February, 2018.

import pandas as pd
import sys, os, csv, shutil, platform, subprocess
sys.path.insert(0, str("F:\\NTM\\src\\"))
import data
from data import edit, select

#     (1-B) Read data and build dataframes for ML

#           Path to data files (CSV-format)

if platform.system() == 'Windows':
 mothur_path = str("F:\\software\\mothur\\mothur.exe")
 data_dir = str("F:\\data\\Subject-05\\")
 data_file = str(data_dir+"mothur_shared.csv")
 shared_file = str(data_dir+"mothur.shared")
 batch_file = str(data_dir+"mothur.batch")
 mothur_single_calculators_file = str(data_dir+"mothur_single_calculators_list.txt")
 mothur_multiple_calculators_file = str(data_dir+"mothur_multiple_calculators_list.txt")
 output_file = str(data_dir+"mothur.out")
#if platform.system() == 'Linux':

data = pd.read_csv(open(data_file,'r'))

mothur_calculators = pd.read_csv(open(mothur_single_calculators_file,'r'))['calculators'].tolist()
for calculator in mothur_calculators:
# print(calculator)
 mothur_cmd = str(' "#summary.single(shared='+shared_file+',calc='+calculator+')"')
 summary_old = str(data_dir+"mothur.groups.summary")
 summary_new = str(data_dir+"mothur."+calculator+".summary")
 call_syntax = str(mothur_path+mothur_cmd)
# print(call_syntax)
 subprocess.call(call_syntax,shell=True)
 command = str("ls -l "+data_dir+"*"+calculator+"*")
 subprocess.call(command,shell=True)
 shutil.move(summary_old,summary_new)
 if calculator == 'jack': calculator = 'jackknife'
 new_column = pd.read_csv(open(summary_new,'r'),sep='\t')[calculator]
 data = pd.concat([data,new_column],axis=1)
 print(data.columns)

mothur_calculators = pd.read_csv(open(mothur_multiple_calculators_file,'r'))['calculators'].tolist()
for calculator in mothur_calculators:
 print(calculator)
 mothur_cmd = str("summary.shared(shared="+shared_file+",calc="+calculator+")")
 summary_old = str(data_dir+"mothur.summary")
 summary_new = str(data_dir+"mothur."+calculator+".summary")
 call_syntax = str(mothur_path+' "#'+mothur_cmd+'"')
 subprocess.call(call_syntax,shell=True)
# shutil.move(summary_old,summary_new)
# new_column = pd.read_csv(open(summary_new,'r'),sep='\t')[calculator]
# print(new_column.columns)