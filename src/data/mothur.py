# This file contains subroutines that act as a wrapper for mothur

# This script creates 'stability.files' for a mothur calculation.
# Requires a '.csv' file with the sample 
# IDs in the first column as input, and the column name 'Sputum_Number'

import pandas, os, glob, subprocess
import os.path, platform, csv, itertools
    
def make_stability_files(sample_list,control_list,stability_files,fastq_dir):
# Read sputum ID numbers
 sample_list = pandas.read_csv(sample_list_file).Sputum_Number
 forward_read_flag = str("L001_R1_001")
 reverse_read_flag = str("L001_R2_001")
 written_list = list()

# Search sub-directories for fastq files with matching sputum ID
 for top,sub_dirs,files in os.walk(fastq_dir):
  continue
# Loop over samples in sample_list
 for sample in itertools.chain(sample_list,control_list):
# Skip files that we already processed
  if not check_sample_list(written_list,sample):
   group,forward_file,reverse_file = '','',''
   group = get_sample_name(sample)
   for file in files:
    if forward_file == '' or reverse_file == '': 
     if forward_read_flag in file: forward_file = str(fastq_dir+file)
     if reverse_read_flag in file: reverse_file = str(fastq_dir+file)
    else if forward_file != '' and reverse_file != '': 
     stability_files.write(group+" "+forward_file+" "+reverse_file+"\n")
     written_list.append(sample)
     break
 return()

def make_batch(stability_files,batch_file,mothur_ref_dir,control_list):
 mothur_lines = list()
 mothur_lines.append(str('pcr.seqs(fasta='+mothur_ref_dir+'silva.bacteria.fasta, start=11894, end=25319, keepdots=F)\n'))
 mothur_lines.append(str('make.contigs(file='+stability_files+', processors=8)\n'))
 mothur_lines.append(str('screen.seqs(fasta=current, group=current, maxambig=0, maxlength=275)\n'))
 mothur_lines.append(str('unique.seqs()'))
 mothur_lines.append(str('count.seqs(name=current, group=current)'))
 mothur_lines.append(str('align.seqs(fasta=current, reference='+mothur_ref_dir+'silva.v4.fasta)\n'))
 mothur_lines.append(str('screen.seqs(fasta=current, count=current, start=1968, end=11550, maxhomop=8)\n'))
 mothur_lines.append(str('filter.seqs(fasta=current, vertical=T, trump=.)\n'))
 mothur_lines.append(str('unique.seqs(fasta=current, count=current)\n'))
 mothur_lines.append(str('pre.cluster(fasta=current, count=current, diffs=2)\n'))
 mothur_lines.append(str('chimera.uchime(fasta=current, count=current, dereplicate=t)\n'))
 mothur_lines.append(str('remove.seqs(fasta=current, accnos=current)\n'))
 mothur_lines.append(str('classify.seqs(fasta=current, count=current, reference='+mothur_ref_dir+'trainset9_032012.pds.fasta, taxonomy='+mothur_ref_dir+'trainset9_032012.pds.tax, cutoff=80)\n'))
 mothur_lines.append(str('remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)\n'))
# remove control groups
 control_groups = format_control_list(control_list)
 mothur_lines.append(str('remove.groups(count=current, fasta=current, taxonomy=current, groups=TDmockD-TDwaterD-PCRwaterA-waterA-waterATD15-PCRwaterB-waterB16-waterBTD15-PCRwaterC-waterC16-zymomockA-zymomockB-zymomockC-ZymomockC2-ZymomockD2)\n'))
 mothur_lines.append(str('classify.seqs(fasta=current, count=current, reference='+mothur_ref_dir+'trainset9_032012.pds.fasta, taxonomy=trainset9_032012.pds.tax, cutoff=80)\n'))
 mothur_lines.append(str('remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)\n'))
 mothur_lines.append(str('remove.groups(count=current, fasta=current, taxonomy=current, groups=Mock)\n'))
 mothur_lines.append(str('cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff=0.15)\n'))
 mothur_lines.append(str('make.shared(list=current, count=current, label=0.03)\n'))
 mothur_lines.append(str('classify.otu(list=current, count=current, taxonomy=current, label=0.03)\n'))
 mothur_lines.append(str('phylotype(taxonomy=current)\n'))
 mothur_lines.append(str('make.shared(list=current, count=current, label=1)\n'))
 mothur_lines.append(str('classify.otu(list=current, count=current, taxonomy=current, label=1)\n'))
 for line in mothur_lines:
  batch_file.write(mothur_line)
 return()
 
def format_control_list(control_list):
 control_string = ''
 for control in control_list: 
  control_string
  control_string.replace(control_string,list(control_string,control))
 return(control_string)
  
def check_sample_list(list_to_check,sample):
 if sample in list_to_check: present = True
 if sample not in list_to_check: present = False
 return(present)
 
def check_sample_filename(filename,sample):
 present = False
 sample,sample_str,sample_str_test1,sample_str_test2,sample_str_test3 = sample,str(sample+'_'),str(sample+'M'),str(sample+'O'),str(sample+'b')
 string_list = list([sample,sample_str,sample_str_test1,sample_str_test2,sample_str_test3])
 for string in string_list:
  if string in filename: present = True
 return(present)
 
def get_sample_name(filename):
 sample_name = filename.split('_')[0]
 sample_name = sample_name.replace('-','')
 return(sample_name)