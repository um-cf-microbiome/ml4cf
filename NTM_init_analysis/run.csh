#! /bin/csh -f
# This file created by Garrett A. Meek on 11-7-17

# This file contains instructions to perform SVM and RF analysis.
# The protocol requires the following external tools:
# 1) libsvm (version 3.22) from:
#    https://www.csie.ntu.edu.tw/~cjlin/libsvm
# 2) A modified version of csv2libsvm.py from: 
#    https://github.com/zygmuntz/phraug
# 3) A modified version of fscore.py from: 
#    https://github.com/caesar0301/wpi-svm
# 
# The tools named above, as well as their paths, are
# referenced in the "USER INPUT" section below.

# Please note the following formatting restrictions for
# the (.csv) data file provided in the "data" path below:
# 1) Data is expected in comma-delimited CSV format
# 2) Only numeric entries are accepted

# USER INPUT
set libsvm = "/mnt/d/software/libsvm-3.22"
set phraug = "/mnt/d/software/phraug-master"
set wpisvm = "/mnt/d/software/wpi-svm-master"
set currentdir = `pwd`
set datadir = "/mnt/d/NTM/data"
set data = "$datadir/ntm-first-positive-dataset-modifiedforpython.csv"
# THESE LOCATIONS ARE COMMENTED OUT IN FAVOR OF VERSIONS MODIFIED FOR LOCAL USE
# set converttolibsvm = "$phraug/csv2libsvm.py"
# set fscore = "$wpisvm/fscore.py"
set converttolibsvm = "$currentdir/tools/csv2libsvm.py"
set fscore = "$currentdir/tools/fscore.py"

# OTHER PROGRAM VARIABLES
# Output file with data formatted for svm analysis
set data_svm = "$currentdir/data.svm"

# CONVERT CSV FILE TO LIBSVM FORMAT:
$converttolibsvm $data $data_svm -1 1

# PERFORM LIBSVM ANALYSIS AND CALCULATE F-SCORE OF SELECTED FEATURES
$fscore $data_svm 
