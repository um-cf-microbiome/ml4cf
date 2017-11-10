# This is an R script to perform principal component analysis (PCA)
# of the first positive NTM dataset for Dr. Lindsay Caverly
# 
# Written by Garrett A. Meek
# November 9, 2017
#
# Read data into variable "rawdata"

rawdata <- read.table("/mnt/d/NTM/data/ntm-first-positive-dataset-modifiedforR.csv",sep=",",header=TRUE)

# Extract columns we are interested in
# data <- rawdata[,"fev1"]

# Perform principal component analysis
prcomp(rawdata,center=TRUE,scale.=TRUE,rank.=3)
