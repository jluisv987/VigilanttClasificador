import pandas as pd
import csv
from sklearn.utils import shuffle
data1 = pd.read_csv('nuevod.csv')
data1 = data1.drop_duplicates(subset=["Groserias"], keep=False)

data2 = pd.read_csv('nuevod2.csv')
data2 = data2.drop_duplicates(subset=["Groserias"], keep=False)


nuevo = pd.concat([data1,data2])
nuevo = shuffle(nuevo)
nuevo.to_csv('nuevod3.csv')
