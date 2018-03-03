# This file contains subroutines that act as a wrapper for mothur

# This script creates 'stability.files' for a mothur calculation.
# Requires a '.csv' file with the sample 
# IDs in the first column as input, and the column name 'Sputum_Number'

import pandas, os, glob, subprocess
import os.path, platform, csv, itertools

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
 command = str('summary.single(calc='+calc_list+')\n')
 return(command)
 
def blast_beta():
 calc_list = ''
 mothur_beta_measures = list(['sharedsobs','sharedchao','sharedace','anderberg','hamming','jclass','jest','kulczynski','kulczynskicody','lennon','ochiai','sorclass','sorest','whittaker','braycurtis','canberra','gower','hellinger','jabund','manhattan','morisitahorn','odum','soergel','sorabund','spearman','speciesprofile','thetan','thetayc'])
 for calculator in mothur_beta_measures:
  if calc_list == '': calc_list = str(calculator)
  else: calc_list = str(calc_list+'-'+calculator)
 command = str('summary.shared(calc='+calc_list+')\n')
 return(command)

def make_batch(stability_files_name,batch_file,mothur_ref_dir,control_list,mothur_output_path):
 level_list = list(['1','2','3'])
 write_list = list()
 write_list.extend([str('pcr.seqs(fasta='+mothur_ref_dir+'silva.bacteria.fasta, start=11894, end=25319, keepdots=F)\n')])
 write_list.extend([str('make.contigs(file='+stability_files_name+', processors=8)\n')])
 write_list.extend([str('get.current()\n')])
 write_list.extend([str('screen.seqs(fasta=current, group=current, maxambig=0, maxlength=275)\n')])
 write_list.extend([str('screen.seqs(fasta=current, group=current, maxambig=0, maxlength=275)\n')])
 write_list.extend([str('unique.seqs()\n')])
 write_list.extend([str('count.seqs(name=current, group=current)\n')])
 write_list.extend([str('align.seqs(fasta=current, reference='+mothur_ref_dir+'silva.v4.fasta,processors=8)\n')])
 write_list.extend([str('screen.seqs(fasta=current, count=current, start=1968, end=11550, maxhomop=8)\n')])
 write_list.extend([str('filter.seqs(fasta=current, vertical=T, trump=.)\n')])
 write_list.extend([str('unique.seqs(fasta=current, count=current)\n')])
 write_list.extend([str('pre.cluster(fasta=current, count=current, diffs=2)\n')])
 write_list.extend([str('chimera.uchime(fasta=current, count=current, dereplicate=t)\n')])
 write_list.extend([str('classify.seqs(fasta=current, count=current, reference='+mothur_ref_dir+'trainset9_032012.pds.fasta, taxonomy='+mothur_ref_dir+'trainset9_032012.pds.tax, cutoff=80)\n')])
 write_list.extend([str('remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)\n')])
# remove control groups
 control_groups = format_control_list(control_list)
 write_list.extend([str('remove.groups(count=current, fasta=current, taxonomy=current, groups='+control_groups+')\n')])
 write_list.extend([str('classify.seqs(fasta=current, count=current, reference='+mothur_ref_dir+'trainset9_032012.pds.fasta, taxonomy='+mothur_ref_dir+'trainset9_032012.pds.tax, cutoff=80)\n')])
 write_list.extend([str('cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff=0.15,processors=4)\n')])
 write_list.extend([str('make.shared(list=current, count=current, label=0.03)\n')])
 write_list.extend([str('classify.otu(list=current, count=current, taxonomy=current, label=0.03)\n')])
 write_list.extend([str('phylotype(taxonomy=current)\n')])
 write_list.extend([blast_alpha()])
 write_list.extend([blast_beta()])
 for level in level_list:
  write_list.extend([str('make.shared(list=current, count=current, label='+level+')\n')])
  write_list.extend([str('classify.otu(list=current, count=current, taxonomy=current, label='+level+')\n')])
  write_list.extend([str('phylotype(taxonomy=current)\n')])
  write_list.extend([blast_alpha()])
  write_list.extend([blast_beta()])
 for line in write_list:
  batch_file.write(line)
 batch_file.close()
 return()
  
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
 
def make_stability_files(sample_list,control_list,stability_files,fastq_dir):
# Read sputum ID numbers
# sample_list = pandas.read_csv(sample_list_file).Sputum_Number
 forward_read_flag = str("L001_R1_001")
 reverse_read_flag = str("L001_R2_001")
 written_list = list()

# Search sub-directories for fastq files with matching sputum ID
 for root,dirs,files in os.walk(fastq_dir):
  continue
# Loop over samples in sample_list 
 for sample in itertools.chain(sample_list,control_list):
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
      stability_files.write(group+" "+forward_file+" "+reverse_file+"\n")
      written_list.append(sample)
      break
 stability_files.close()
 return
 
def cmd_line(mothur_path,batch_file_path,mothur_output_path):
 mothur_command = str(mothur_path+' '+batch_file_path+' > '+mothur_output_path+'mothur.out')
 return(mothur_command)
 
def run(mothur_command):
 subprocess.call(mothur_command,shell=True)
 return
 
