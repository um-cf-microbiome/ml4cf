# This script reads a CSV file to an array
import sys
import pandas as pandas
import os
import numpy as np
from scipy.stats import linregress
import math
import io

def read_array(datafile):
 print('Reading data from '+datafile)
 with io.open(datafile,'r',newline="") as dataread:
  data=[[0.0 for i in range(0,len(columns))]]
  for row_tuple in dataread:
   row=np.array(row_tuple.strip().split(','))
   data=np.vstack((data,row))
 data=np.delete(data,(0),axis=0)
 return data
