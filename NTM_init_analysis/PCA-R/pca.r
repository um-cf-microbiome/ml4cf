library(plot3D)
require(graphics)
# This is an R script to perform principal component analysis (PCA)
# of the first positive NTM dataset for Dr. Lindsay Caverly
# 
# Written by Garrett A. Meek
# November 9, 2017
#
# Read data into variable "rawdata"

data <- read.table("/mnt/d/NTM/data/ntm-first-positive-dataset-modifiedforR.csv",sep=",",header=TRUE)

# Perform principal component analysis
# Documentation for prcomp() provided at:
# https://www.rdocumentation.org/packages/stats/versions/3.4.1/topics/prcomp
#
pcaoutput <- prcomp(data,center=TRUE,scale.=TRUE,retx=TRUE,rank.=3)
# Convert output to a more user-friendly format
stdev <- matrix(unlist(pcaoutput[1]))
#stdev is a vector containing the standard deviation of 
rotation <- matrix(unlist(pcaoutput[2]), ncol = ncol(data), byrow=TRUE)
#rotation is an ncol(data) X ncol(data) rotation matrix
center <- matrix(unlist(pcaoutput[3]))
#center is a vector containing the coordinate center for the rotated (principal component space)
scale <- matrix(unlist(pcaoutput[4]))
#scale is a vector containing the scaling factors for all features in the space of the rotated principal components
pcs <- matrix(unlist(pcaoutput[5]), ncol = ncol(data), byrow=TRUE)
topthreepcs <- pcs[,1:3]
file.create("/mnt/d/NTM/NTM_init_analysis/PCA/PCA.csv",overwrite=TRUE)
write("This file contains the top three principal components from PCA",file="/mnt/d/NTM/NTM_init_analysis/PCA/PCA.csv",)
for (i in nrow(topthreepcs)){
 write(topthreepcs[i],file="/mnt/d/NTM/NTM_init_analysis/PCA/PCA.csv")
}
# pcaoutput contains:
# 1) stdev. for principal components (PCs)
# 2) Rotation vectors to transform current features into PCs
# 3) The center of the principal component coordinates
# 4) The scale used for each feature (when rescaling values for unweighted PCA)
# 5) The principal components (listed as vectors with the same length as the number of features in the data list (number of columns: ncol(data)

# Plot the result
#, lab = FALSE, title = "NTM PCA", xlim = NULL, ylim = NULL, new.plot = TRUE, pdf.file = "/mnt/d/NTM/NTM_init_analysis/PCA/scree-pca.pdf")
