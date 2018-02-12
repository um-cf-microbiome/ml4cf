# This file contains wrapper subroutines for Mothur

import subprocess, platform

def run_mothur():
# This subroutine calls mothur
 if platform.system() == 'Windows':
  mothur_path = "F:\\software\\mothur\\mothur.exe"
  batch_file = "F:\\NTM\\analysis\\mothur\\stability.batch"
  output_file = "F:\\NTM\\analysis\\mothur\\mothur.out"
  silva_fasta_ref = "F:\\NTM\\analysis\\mothur\\silva.bacteria.fasta"
 
# Build the mothur .batch file
  pcr.seqs(fasta=silva.bacteria.fasta, start=11894, end=25319, keepdots=F)

make.contigs(file=stability.files, processors=4)
screen.seqs(fasta=current, group=current, maxambig=0, maxlength=275)
unique.seqs()
count.seqs(name=current, group=current)
align.seqs(fasta=current, reference=silva.v4.fasta)
screen.seqs(fasta=current, count=current, start=1968, end=11550, maxhomop=8)
filter.seqs(fasta=current, vertical=T, trump=.)
unique.seqs(fasta=current, count=current)
pre.cluster(fasta=current, count=current, diffs=2)
chimera.uchime(fasta=current, count=current, dereplicate=t)
remove.seqs(fasta=current, accnos=current)
classify.seqs(fasta=current, count=current, reference=trainset9_032012.pds.fasta, taxonomy=trainset9_032012.pds.tax, cutoff=80)
remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)
remove.groups(count=current, fasta=current, taxonomy=current, groups=Mock)
cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff=0.15)
make.shared(list=current, count=current, label=0.03)
classify.otu(list=current, count=current, taxonomy=current, label=0.03)
phylotype(taxonomy=current)
make.shared(list=current, count=current, label=1)
classify.otu(list=current, count=current, taxonomy=current, label=1)

 call_syntax = str(mothur_path+" "+batch_file+" > "+output_file)
 subprocess.call(call_syntax,shell=True)
 return()
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe","F:\\NTM\\analysis\\mothur\\stability.batch",">","F:\\NTM\\analysis\\mothur\\mothur.out"])
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe < F:\\NTM\\analysis\\mothur\\stability.batch > F:\\NTM\\analysis\\mothur\\mothur.out"])