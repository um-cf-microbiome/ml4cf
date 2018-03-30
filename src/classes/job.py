import os

class info(object):
     def __init__(self,job_name,job_dir,host_info,control_list_file=None):
      self.job_name = job_name
      self.job_dir = job_dir
      self.host_base = host_info.host_base
      self.mothur_path = host_info.mothur_path
      self.processors = host_info.processors
      self.classifiers = list(['NTM_disease','Persistent_infection'])
      self.class_options = list([['TRUE','FALSE'],['TRUE','FALSE']])
      self.sample_list_file = open(str(self.job_dir+'/sample_list.csv'),'r')
      if control_list_file != None:
       if control_list_file == True:
        self.control_list_file = open(str(self.job_dir+'/control_sample_list.csv'),'r')
       if control_list_file != True:
        self.control_list_file = open(str(self.job_dir+'/'+self.control_list_file),'r')
          
      self.mothur_ref_dir=str(self.host_base+"data/fastq_files/ref/")
      self.job_fastq_dir=str(self.host_base+"data/fastq_files/lab/")
      self.mothur_output_path=str(self.job_dir+"/analysis/mothur/")
      if not os.path.exists(self.mothur_output_path):
       os.makedirs(self.mothur_output_path)
      self.stability_files = open(str(self.job_dir+'/analysis/mothur/'+job_name+'.files'),'w')
      self.batch_file_name = str(self.job_dir+'/analysis/mothur/'+job_name+'.batch')
      self.batch_file=open(self.batch_file_name,'w')
      self.mothur_output_file=str(self.job_dir+"/analysis/mothur/mothur_"+job_name+".out")
      self.sample_list = list()
      self.control_list = list()

def clean(object):
    if os.path.exists(object.mothur_output_file): os.remove(object.mothur_output_file)
    return