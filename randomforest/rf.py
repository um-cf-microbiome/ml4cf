from io import StringIO
import pandas as pd
import sklearn.ensemble as sk
from sklearn.ensemble import RandomForestClassifier
microbiome_data = '/mnt/d/NTM/randomforest/microbiome_only.csv'
clinical_data = '/mnt/d/NTM/randomforest/clinicaldata.csv'
biome = pd.read_csv(microbiome_data, header=None)
clinical = pd.read_csv(clinical_data)
classifier=RandomForestClassifier(n_estimators=50)
clinical_test = clinical[0]
print(clinical_test.shape)
print(biome.shape)
classifier=classifier.fit(biome,clinical)
print(classifier)
