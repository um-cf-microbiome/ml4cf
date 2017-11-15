# This code is designed to perform principal component analysis (PCA) 
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
# Select PCA using three components
print data.shape
pca=PCA(n_components=num_components)
# Find principal components for and then
# transform 'data' into properly-formatted array (data_pca)
# data = data_points (rows) X features (columns) array
# data_pca = features (rows) X principal components (columns) array
data_pca=np.array(pca.fit_transform(data),dtype=float)
for i in range(len(data_pca)):
 for j in range(len(data_pca[0])):
  data_pca[i,j]=float(data_pca[i,j])
#
# Write the PCA output to output file
#
#print features.T.shape
#print data_pca.shape
data_out=np.hstack([features.T,data_pca.T])
#print data_out.shape
np.savetxt(outputfile,data_out,fmt="%10s")
quit()
