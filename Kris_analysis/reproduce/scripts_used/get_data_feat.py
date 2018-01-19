# This script reads data from a csv file, and
# creates a pandas dataframe containing
# the fields of data defined in 'data_to_keep'
import pandas as pd
import sys

data_file = sys.argv[1]
#These fields are pulled from 'data_file' and used for analysis
features_file = sys.argv[2]

trim_data_file = sys.argv[3]

# Read data and feature selections
data = pd.read_csv(data_file,header=None)
data_header = pd.read_csv(data_file)
keep = pd.read_csv(features_file)
old_data = pd.DataFrame(data_header['sample'])
#Keep the first row with the feature names
#final_data = data.iloc[0,:]

for want in keep['feature_list']:
 for check in data.iloc[0,:]:
  if (want == check) and (want != 'sample'):
   new_feature = pd.DataFrame(data_header[want])
   final_data = old_data.join(new_feature)
   old_data = final_data

final_data.to_csv(trim_data_file,index=False)
quit()
