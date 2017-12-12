import os
import sys

#combine.py > output.csv

in1 = file('cav_dataset_subset.csv','r')

in2 = file('long_feat.csv','r')

dd = {}


for line in in2:
    cells = line.split(',')
    dd[cells[0]] = cells

in2.close()

for line in in1:
    cells = line.split(',')
    if cells[1] != 'patient_id':
        outer = line.strip() + ',' + ','.join(dd[cells[1]][1:])
        outer.strip()
        print outer