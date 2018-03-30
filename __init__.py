import os
# Import 'ml4cf' modules
module_list = []
for (dirpath,dirnames,filenames) in os.walk(os.getcwd()+'/src'):
 if '.git' and 'pycache' not in dirnames:
  module_list.extend(dirnames)
  break
for module_name in module_list:
 import src.module_name as module_name
