import pandas as pd
import csv
from sklearn.utils import shuffle
data1 = pd.read_csv('Dataset1.csv')
data1 = data1.drop_duplicates(subset=["Groserias"], keep=False)

data2 = pd.read_csv('Dataset2.csv')
data2 = data2.drop_duplicates(subset=["Groserias"], keep=False)


nuevo = pd.concat([data1,data2])
nuevo = shuffle(nuevo)
nuevo.to_csv('Completo.csv')
