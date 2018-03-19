import os.path, subprocess, sys

def old_files(job_info):
# Remove data files from old run

 if sys.platform == 'win32':
  if os.path.isfile(job_info.mothur_output_file): 
   subprocess.call('del '+job_info.mothur_output_file)
  if os.path.isfile(job_info.stability_files_name): 
   subprocess.call('del '+job_info.stability_files_name)
  if os.path.isfile(job_info.batch_file_name): 
   subprocess.call('del '+job_info.batch_file_name)
 return