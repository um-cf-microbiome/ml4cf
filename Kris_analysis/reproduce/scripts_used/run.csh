#! /bin/csh -f
# This script executes Kris' SVM analysis of NTM data using the proper
# command-line arguments. This script should allow reproduction
# of his SVM (F-score) analysis.

# Provide the path to a csv file with data
set csv_data_file = '/mnt/d/NTM/data/ntm-first-positive-dataset-full.csv'
set output_file = '/mnt/d/NTM/data/Castner_sequences/svm.out'

# Calculate slope and intercepts from linear regression of data
python lin_reg.py $csv_data_file > $output_file
exit

# Convert the data to format that we can use with 'libsvm' package
python csv2libsvm.py $csv_data_file data.svm -1 1 >> $output_file

# Perform SVM analysis and calculate F-score for each of the features in the data file.
python fscore.py data.svm >> $output_file
