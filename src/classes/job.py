class info(object):
     def __init__(self,job_name,host_info):
      self.job_name = job_name
      self.host_base = host_info.host_base
      self.mothur_path = host_info.mothur_path
      self.processors = host_info.processors
      self.classifiers = list(['NTM_disease','Persistent_infection'])
      self.class_options = list([['TRUE','FALSE'],['TRUE','FALSE']])
      self.run_base = str(host_base+"NTM/")
      self.sample_list_file = open(str(host_base+'NTM/analysis/sample_list.csv'),'r')
      self.control_list_file_name = str(host_base+'NTM/analysis/control_sample_list.csv')
      self.control_list_file = open(self.control_list_file_name,'r')
      self.mothur_ref_dir=str(host_base+"data/fastq_files/ref/")
      self.job_fastq_dir=str(host_base+"data/fastq_files/lab/")
      self.stability_files_name = str(host_base+'NTM/analysis/mothur/stability.files')
      self.stability_files=open(self.stability_files_name,'w')
      self.batch_file_name = str(host_base+'NTM/analysis/mothur/stability.batch')
      self.batch_file=open(self.batch_file_name,'w')
      self.mothur_output_path=str(host_base+"NTM/analysis/mothur/")
      self.mothur_output_file=str(host_base+"NTM/analysis/mothur/mothur.out")
      self.sample_list = list()
      self.control_list = list()
