# This code is designed to perform support vector machine (SVM) analysis
# of the first positive NTM data set from Dr. Lindsay Caverly.

# Written by Garrett A. Meek on
# November 13, 2017

# Load necessary python modules
import csv
import io
# numpy used for some matrix operations
import numpy as np
# the following used for plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import figure, show
# sklearn 'decomposition' used for PCA
from sklearn.decomposition import PCA
# Path to file containing NTM data
datafile='/mnt/d/NTM/data/ntm-first-positive-dataset-modifiedforpython.csv'
outputfile='/mnt/d/NTM/NTM_init_analysis/PCA/PCA.dat'
num_components=107

with io.open(datafile,'r',newline="") as dataread:
 columns=dataread.readline().strip().split(',')
# Create an empty array for our data
 data=[[0.0 for i in range(len(columns))]]
# Read data from 'datafile'
 features=np.array([columns],dtype=str)
 for row_tuple in dataread:
  row=np.array(row_tuple.strip().split(','),dtype=float)
  data=np.vstack((data,row))
# transform 'data' into properly-formatted array 
# data = features (rows) X principal components (columns) array
data=np.array(data,dtype=float)
#
# Write SVM output to output file
#
#print features.T.shape
#print data_pca.shape
data_out=np.hstack([features.T,data_svm])
#print data_out.shape
np.savetxt(outputfile,data_out,fmt="%10s")
quit()
