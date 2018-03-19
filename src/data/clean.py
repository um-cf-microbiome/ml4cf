import os, subprocess

def old_files(run_info):
# Remove data files from old run
 if os.path.isfile(run_info.mothur_output_file): 
  print(run_info.mothur_output_file)
  subprocess.call('del '+run_info.mothur_output_file)
 if os.path.isfile(run_info.stability_files_name): 
  print(run_info.stability_files_name)
  subprocess.call('del '+run_info.stability_files_name)
 if os.path.isfile(run_info.batch_file_name): 
  print(run_info.batch_file_name)
  subprocess.call('del '+run_info.batch_file_name)
 return