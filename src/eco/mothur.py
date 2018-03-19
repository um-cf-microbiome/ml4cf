# This file contains subroutines that act as a wrapper for mothur

# This script creates 'stability.files' for a mothur calculation.
# Requires a '.csv' file with the sample 
# IDs in the first column as input, and the column name 'Sputum_Number'

import os, glob, subprocess
import os.path, platform, csv, itertools
import pandas as pd
global mothur_output_files

def get_group(sample_name):
 sample_group = sample_name.split('_')[0]
 sample_group = sample_group.replace('-','')
 return(sample_group)

def format_control_list(control_list):
 control_string = ''
 for control in control_list:
  if control_string == '':
   control_string = str(control)
  else:
   append = str('-'+get_group(control))
   control_string = str(control_string+append)
 return(control_string)
 
def blast_alpha():
 calc_list = ''
 mothur_alpha_measures = list(['sobs','chao','ace','jack','bootstrap','simpsoneven','shannoneven','heip','smithwilson','bergerparker','shannon','npshannon','simpson','invsimpson','coverage','qstat','boneh','efron','shen','solow','logseries','geometric','bstick'])
 for calculator in mothur_alpha_measures:
  if calc_list == '': calc_list = str(calculator)
  else: calc_list = str(calc_list+'-'+calculator)
 command = str('summary.single(calc='+calc_list+')')
 return(command)
 
def blast_beta():
 calc_list = ''
 mothur_beta_measures = list(['sharedsobs','sharedchao','sharedace','anderberg','hamming','jclass','jest','kulczynski','kulczynskicody','lennon','ochiai','sorclass','sorest','whittaker','braycurtis','canberra','gower','hellinger','jabund','manhattan','morisitahorn','odum','soergel','sorabund','spearman','speciesprofile','thetan','thetayc'])
 for calculator in mothur_beta_measures:
  if calc_list == '': calc_list = str(calculator)
  else: calc_list = str(calc_list+'-'+calculator)
 command = str('summary.shared(calc='+calc_list+')')
 return(command)

def mothur_command_list(level_list,mothur_ref_dir,mothur_output_path,processors,control_list):
 print(mothur_output_path)
 input_command_list = list()
 output_file_list = list()
 if not os.path.isfile(mothur_output_path+'silva.v4.fasta'):
  if os.path.isfile(mothur_ref_dir+'silva.v4.fasta'):
   run('mv '+mothur_ref_dir+'silva.v4.fasta '+mothur_output_path+'silva.v4.fasta')
  if not os.path.isfile(mothur_ref_dir+'silva.v4.fasta'):
   output_file_list.append(["silva.bacteria.pcr.fasta"])
   input_command_list.extend([str('pcr.seqs(fasta='+mothur_ref_dir+'silva.bacteria.fasta, start=11894, end=25319, keepdots=F)')])
   output_file_list.append(["silva.v4.fasta"])
   input_command_list.extend([str('system(mv '+mothur_output_path+'silva.bacteria.pcr.fasta '+mothur_output_path+'silva.v4.fasta)')])
 output_file_list.append(["stability.trim.contigs.fasta","stability.trim.contigs.qual","stability.contigs.report","stability.scrap.contigs.fasta","stability.scrap.contigs.qual","stability.contigs.groups"])
 input_command_list.extend([str('make.contigs(file='+mothur_output_path+'stability.files, processors='+str(processors)+')')])
 output_file_list.append(["stability.trim.contigs.good.fasta","stability.trim.contigs.bad.accnos","stability.contigs.good.groups"])
 input_command_list.extend([str('screen.seqs(fasta='+mothur_output_path+'stability.trim.contigs.fasta, group='+mothur_output_path+'stability.contigs.groups, maxambig=0, maxlength=275)')])
 output_file_list.append(["stability.trim.contigs.good.names","stability.trim.contigs.good.unique.fasta"])
 input_command_list.extend([str('unique.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.fasta)')])
 output_file_list.append(["stability.trim.contigs.good.count_table"])
 input_command_list.extend([str('count.seqs(name='+mothur_output_path+'stability.trim.contigs.good.names, group='+mothur_output_path+'stability.contigs.good.groups)')])
 output_file_list.append(["stability.trim.contigs.good.unique.align","stability.trim.contigs.good.unique.align.report","stability.trim.contigs.good.unique.flip.accnos"])
 input_command_list.extend([str('align.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.fasta, reference='+mothur_ref_dir+'silva.v4.fasta,processors='+str(processors)+')')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.align","stability.trim.contigs.good.unique.bad.accnos","stability.trim.contigs.good.good.count_table"])
 input_command_list.extend([str('screen.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.fasta, count='+mothur_output_path+'stability.trim.contigs.good.count_table, start=1968, end=11550, maxhomop=8)')])
 output_file_list.append(["stability.filter","stability.trim.contigs.good.unique.good.filter.fasta"])
 input_command_list.extend([str('filter.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.align, vertical=T, trump=.)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.count_table","stability.trim.contigs.good.unique.good.filter.unique.fasta"])
 input_command_list.extend([str('unique.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.fasta, count='+mothur_output_path+'stability.trim.contigs.good.good.filter.count_table)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta","stability.trim.contigs.good.unique.good.filter.unique.precluster.count_table"])
 input_command_list.extend([str('pre.cluster(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.fasta, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.count_table, diffs=2)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.chimeras","stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table","stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.accnos"])
 input_command_list.extend([str('chimera.uchime(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.count_table, dereplicate=t)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.tax.summary"])
 input_command_list.extend([str('classify.seqs(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table, reference='+mothur_ref_dir+'trainset9_032012.pds.fasta, taxonomy='+mothur_ref_dir+'trainset9_032012.pds.tax, cutoff=80)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.taxonomy","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta","stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table"])
 input_command_list.extend([str('remove.lineage(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.fasta, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table, taxonomy='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.taxonomy, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.fasta","stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy"])
 input_command_list.extend([str('remove.groups(count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table, fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta, taxonomy='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.taxonomy, groups='+format_control_list(control_list)+')')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.dist","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.sensspec"])
 input_command_list.extend([str('cluster.split(fasta='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.fasta, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, taxonomy='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy, splitmethod=classify, taxlevel=4, cutoff=0.15, processors=4, large=T)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.shared"])
 input_command_list.extend([str('make.shared(list='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, label=0.03)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.0.16.cons.taxonomy","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.0.16.cons.tax.summary"])
 input_command_list.extend([str('classify.otu(list='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list, count='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, taxonomy='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy, label=0.03)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.sabund","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.rabund","stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.list"])
 input_command_list.extend([str('phylotype(taxonomy='+mothur_output_path+'stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy)')])
 output_file_list.append(["stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.groups.summary"])
 input_command_list.extend([blast_alpha()])
# input_command_list.extend([blast_beta()])
# for level in level_list:
#  input_command_list.extend([str('classify.otu(list=current, count=current, taxonomy=current, label='+level+')')])
#  input_command_list.extend([str('make.shared(list=current, count=current, label='+level+')')])
#  input_command_list.extend([str('phylotype(taxonomy=current)')])
#  input_command_list.extend([blast_alpha()])
#  input_command_list.extend([blast_beta()])
 return(input_command_list,output_file_list)

def batch(job_info):
 level_list = list(['1','2','3'])
 input_command_list,output_file_list = mothur_command_list(level_list,job_info.mothur_ref_dir,job_info.mothur_output_path,job_info.processors,job_info.control_list)
 index=0
 for command in input_command_list:
#  output_files = list([str(mothur_output_path+output_file_list[index][i]) for i in output_file_list[index]])
  for output_filename in output_file_list[index]:
   output = job_info.mothur_output_file
   if not os.path.isfile(output) or (os.path.isfile(output) and os.stat(output).st_size == 0):
     zip_filename = str(output+".zip")
     if not os.path.isfile(zip_filename):
      append_batch_run(job_info,command)
  index = index + 1
 return
  
def check_sample_list(list_to_check,sample):
 if sample in list_to_check: present = True
 if sample not in list_to_check: present = False
 return(present)
 
def check_sample_str(filename,sample):
 present = False
 sample_str,sample_str_test1,sample_str_test2,sample_str_test3 = str(sample+'_'),str(sample+'M'),str(sample+'O'),str(sample+'b')
 string_list = list([sample_str,sample_str_test1,sample_str_test2,sample_str_test3])
 for string in string_list:
  if string in filename: present = True
 return(present)
 
def make_stability_files(job_info):
# Read sputum ID numbers
# sample_list = pandas.read_csv(sample_list_file).Sputum_Number
 forward_read_flag = str("L001_R1_001")
 reverse_read_flag = str("L001_R2_001")
 written_list = list()

# Search sub-directories for fastq files with matching sputum ID
 print(job_info.mothur_ref_dir)
 for root,dirs,files in os.walk(job_info.mothur_ref_dir):
  continue
# Loop over samples in sample_list 
 for sample in itertools.chain(job_info.sample_list,job_info.control_list):
# Skip files that we already processed
  if not check_sample_list(written_list,sample):
   group,forward_file,reverse_file = '','',''
   group = get_group(sample)
   for file in files:
    if check_sample_str(file,sample) and ('.fastq' in file):
     if forward_file == '' and forward_read_flag in file: 
      forward_file = str(fastq_dir+file)
     if reverse_file == '' and reverse_read_flag in file: 
      reverse_file = str(fastq_dir+file)

     if forward_file != '' and reverse_file != '': 
      job_info.stability_files.write(group+" "+forward_file+" "+reverse_file+"\n")
      written_list.append(sample)
      break
 job_info.stability_files.close()
 return
 
def run(mothur_command):
# System call of mothur executable with "mothur_command"
 if '#' in mothur_command:
  print( mothur_command.split('#',1)[1].split('(',1)[0])
 subprocess.call(mothur_command,shell=True)
 return

def append_batch_run(job_info,command):
# This subroutine runs a mothur command if the
# anticipated output files are missing.
 batch_path = str(job_info.batch_file_name)
 if os.path.isfile(batch_path): batch = open(batch_path,'a')
 if not os.path.isfile(batch_path): batch = open(batch_path,'w')
 cmd = str(command+'\n')
 batch.write(cmd)
 batch.close()
 if not os.path.isfile(job_info.mothur_output_file): command = str(job_info.mothur_path+' "#'+command+'" > '+job_info.mothur_output_file)
 if os.path.isfile(job_info.mothur_output_file): command = str(job_info.mothur_path+' "#'+command+'" >> '+job_info.mothur_output_file)
 run(command)
 return
  
