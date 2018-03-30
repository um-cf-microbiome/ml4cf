# This file contains wrapper subroutines for 'mothur'

import os, glob, subprocess, shutil
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

def mothur_command_list(job_info):
 level_list = list(['0','1','2','3'])
 job_name = job_info.job_name
 job_path = job_info.mothur_output_path
 ref_path = job_info.mothur_ref_dir
 processors = job_info.processors
 input_command_list = list()
 output_file_list = list()
 if not os.path.isfile(ref_path+'silva.v4.fasta'):
  output_file_list.append(["silva.bacteria.pcr.fasta"])
  input_command_list.extend([str('pcr.seqs(fasta='+ref_path+'silva.bacteria.fasta, start=11894, end=25319, keepdots=F)')])
  output_file_list.append(["silva.v4.fasta"])
  input_command_list.extend([str('system(mv '+job_path+'silva.bacteria.pcr.fasta '+ref_path+'silva.v4.fasta)')])
 output_file_list.append([str(job_name+".trim.contigs.fasta"),str(job_name+".trim.contigs.qual"),str(job_name+".contigs.report"),str(job_name+".scrap.contigs.fasta"),str(job_name+".scrap.contigs.qual"),str(job_name+".contigs.groups")])
 input_command_list.extend([str('make.contigs(file='+job_path+job_name+'.files, processors='+str(processors)+')')])
 output_file_list.append([str(job_name+".trim.contigs.good.fasta"),str(job_name+".trim.contigs.bad.accnos"),str(job_name+".contigs.good.groups")])
 input_command_list.extend([str('screen.seqs(fasta='+job_path+job_name+'.trim.contigs.fasta, group='+job_path+job_name+'.contigs.groups, maxambig=0, maxlength=275)')])
 output_file_list.append([str(job_name+".trim.contigs.good.names"),str(job_name+".trim.contigs.good.unique.fasta")])
 input_command_list.extend([str('unique.seqs(fasta='+job_path+job_name+".trim.contigs.good.fasta)")])
 output_file_list.append([str(job_name+".trim.contigs.good.count_table")])
 input_command_list.extend([str('count.seqs(name='+job_path+job_name+'.trim.contigs.good.names, group='+job_path+job_name+'.contigs.good.groups)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.align"),str(job_name+".trim.contigs.good.unique.align.report"),str(job_name+".trim.contigs.good.unique.flip.accnos")])
 input_command_list.extend([str('align.seqs(fasta='+job_path+job_name+'.trim.contigs.good.unique.fasta, reference='+ref_path+'silva.v4.fasta,processors='+str(processors)+')')])
 output_file_list.append([str(job_name+'.trim.contigs.good.unique.good.fasta'),str(job_name+".trim.contigs.good.unique.bad.accnos"),str(job_name+".trim.contigs.good.good.count_table")])
 input_command_list.extend([str('screen.seqs(fasta='+job_path+job_name+'.trim.contigs.good.unique.fasta, count='+job_path+job_name+'.trim.contigs.good.count_table, start=1968, end=11550, maxhomop=8)')])
 output_file_list.append([str(job_name+".filter"),str(job_name+".trim.contigs.good.unique.good.filter.fasta")])
 input_command_list.extend([str('filter.seqs(fasta='+job_path+job_name+'.trim.contigs.good.unique.align, vertical=T, trump=.)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.count_table"),str(job_name+".trim.contigs.good.unique.good.filter.unique.fasta")])
 input_command_list.extend([str('unique.seqs(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.fasta, count='+job_path+job_name+'.trim.contigs.good.good.filter.count_table)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.fasta"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.count_table")])
 input_command_list.extend([str('pre.cluster(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.fasta, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.count_table, diffs=2)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.chimeras"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.accnos")])
 input_command_list.extend([str('chimera.uchime(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.fasta, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.count_table, dereplicate=t)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.fasta"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.tax.summary")])
 input_command_list.extend([str('classify.seqs(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.fasta, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table, reference='+ref_path+'trainset9_032012.pds.fasta, taxonomy='+ref_path+'trainset9_032012.pds.tax, cutoff=80)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.taxonomy"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table")])
 input_command_list.extend([str('remove.lineage(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.fasta, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.count_table, taxonomy='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.taxonomy, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.fasta"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy")])
 input_command_list.extend([str('remove.groups(count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table, fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta, taxonomy='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.taxonomy, groups='+format_control_list(job_info.control_list)+')')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.dist"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.sensspec")])
 input_command_list.extend([str('cluster.split(fasta='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.fasta, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, taxonomy='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy, splitmethod=classify, taxlevel=4, cutoff=0.15, processors='+str(processors)+', large=T)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.shared")])
 input_command_list.extend([str('make.shared(list='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, label=0.03)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.0.16.cons.taxonomy"),str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.0.16.cons.tax.summary")])
 input_command_list.extend([str('classify.otu(list='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.pick.opti_mcc.unique_list.list, count='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.pick.count_table, taxonomy='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy, label=0.03)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.sabund"),str("job_name.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.rabund"),str("job_name.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.list")])
 input_command_list.extend([str('phylotype(taxonomy='+job_path+job_name+'.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.taxonomy)')])
 output_file_list.append([str(job_name+".trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.pick.pick.tx.groups.summary")])
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
 input_command_list,output_file_list = mothur_command_list(job_info)
 index=0
 for command in input_command_list:
  output_files = list(output_file_list[index])
  for output in output_file_list[index]:
   if not os.path.isfile(output):
    zip_filename = str(output+'.zip')
    if not os.path.isfile(zip_filename):
     print('Missing '+output+'. Running '+command)
     append_batch_run(job_info,command)
     if not os.path.isfile(output):
      job_info.batch_file.close()
      print("Batch job failed during the following command:")
      print(command)
      quit()
     else:
      break
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

 for root,dirs,files in os.walk(job_info.job_fastq_dir):
  continue
# Loop over samples in sample_list 
 for sample in itertools.chain(job_info.sample_list,job_info.control_list):
# Skip files we already processed
  if not check_sample_list(written_list,sample):
   group,forward_file,reverse_file = '','',''
   group = get_group(sample)
   for file in files:
    if check_sample_str(file,sample) and ('.fastq' in file):
     if forward_file == '' and forward_read_flag in file: 
      forward_file = str(job_info.job_fastq_dir+file)
     if reverse_file == '' and reverse_read_flag in file: 
      reverse_file = str(job_info.job_fastq_dir+file)

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
 if not os.path.isfile(job_info.mothur_output_file): command = str(job_info.mothur_path+' "#'+command+'" > '+job_info.mothur_output_file)
 if os.path.isfile(job_info.mothur_output_file): command = str(job_info.mothur_path+' "#'+command+'" >> '+job_info.mothur_output_file)
 run(command)
 return
  
