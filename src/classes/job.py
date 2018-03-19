class job(object):

 def __init__(self,host_base,mothur_path,R_path,processors):
     self.host_base = host_base
     self.mothur_path = mothur_path
     self.R_path = R_path
     self.processors = processors
     classifiers=list(['NTM_disease','Persistent_infection'])
     classes=list([['TRUE','FALSE'],['TRUE','FALSE']])
     run_base=str(host_base+"NTM/")
     sample_list_file=open(str(host_base+'NTM/analysis/sample_list.csv'),'r')
     control_list_file_name = str(host_base+'NTM/analysis/control_sample_list.csv')
     control_list_file = open(control_list_file_name,'r')
     fastq_dir=str(host_base+"data/fastq_files/")
     mothur_ref_dir=str(host_base+"data/fastq_files/")
     stability_files_name = str(host_base+'NTM/analysis/mothur/stability.files')
     stability_files=open(stability_files_name,'w')
     batch_file_name = str(host_base+'NTM/analysis/mothur/stability.batch')
     batch_file=open(batch_file_name,'w')
     mothur_output_path=str(host_base+"NTM/analysis/mothur/")
     mothur_output_file=str(host_base+"NTM/analysis/mothur/mothur.out")
     return(self.host_base,self.mothur_path,self.R_path,self.processors)

 global classifiers, classes, run_base
 global sample_list_file, control_list_file, control_list_file_name
 global fastq_dir, mothur_ref_dir, stability_files_name
 global stability_files, batch_file_name, batch_file
 global mothur_output_path, mothur_output_file
 global processors, R_path, host_base, mothur_path