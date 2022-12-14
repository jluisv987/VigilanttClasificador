# -*- coding: utf-8 -*-
"""ngramas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g6UlmeE2z-JXiDb-vR1BpMaA__yCMvIf
"""

!pip install unidecode

!python -m spacy download es_core_news_md

from io import IncrementalNewlineDecoder
import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from sklearn.utils import shuffle
import pandas as pd
import re
import numpy as np
import es_core_news_md
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
import unidecode
import unicodedata
import warnings
warnings.filterwarnings('ignore')
#spacy
stop_words_spacy = list(STOP_WORDS)

print(stop_words_spacy)

data = pd.read_csv('/nuevod3.csv')
data = data.drop_duplicates(subset=["Groserias"], keep=False)
data.head(15)

#data = shuffle(data)
#data.head(15)

# Removing stopwords in a string
palabras_parada = []
nlp = spacy.load('es_core_news_md')

def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in (palabras_parada)])
    return text
 
#Lemmatizing the text in a string
def lemmatize_text(text):
    text = [word.lemma_ for word in nlp(text)]
    text = ' '.join(text)
    return text


#substituting accents in a string
def remove_accents(text):
    
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    
    return text


#removing twitter users in a string
def remove_users(text):
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())

    return text

#removing urls in a string
def remove_urls(text):
    text = re.sub(r'http\S+','',text)
    return text

# Text to lowercase in a string
def text_to_lowercase(text):
    text = text.lower()
    return text

#removing numbers in a string
def remove_numbers(text):
    text = re.sub(r'\d+','',text)
    return text


#removing special characters in a string
def remove_special_characters(text):
    text = re.sub(r'[^\w\s]','',text)
    return text

for palabra in spacy.lang.es.stop_words.STOP_WORDS:
    palabras_parada.append(remove_accents(palabra))

# Cleaning the text
def clean_text(text):
    text = remove_accents(text)

    text = remove_users(text)
    
    text = remove_urls(text)
    
    text = remove_numbers(text)
    
    #text = remove_special_characters(text)
    
    text = text_to_lowercase(text)
    #text = remove_stopwords(text)
    text = lemmatize_text(text)
    #print(text)

    return text

data["Groserias"] = data["Groserias"].apply(clean_text)
data.head(15)

"""# Secci??n nueva"""

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report,roc_auc_score
from sklearn.linear_model import LogisticRegression

tfidf = TfidfVectorizer(max_features=5000)
data = shuffle(data)
X = data['Groserias']
y = data['Ofensivo']
X = tfidf.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=50)

clf = LogisticRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test,y_pred))

dato = clean_text("buenos dias como estas el dia de hoy")

vec = tfidf.transform([dato])

print(clf.predict(vec))

print(X_train)

X = data['Groserias']
y = data['Ofensivo']
#X = tfidf.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=50)
vect = CountVectorizer(ngram_range=(1,3)).fit(X_train)
X_train_vectorized = vect.transform(X_train)
clf = LogisticRegression()
clf.fit(X_train_vectorized, y_train)
predictions = clf.predict(vect.transform(X_test))
print(roc_auc_score(y_test,predictions))

feature_names = np.array(vect.get_feature_names())
sorted_coef_index = clf.coef_[0].argsort()

print(feature_names[sorted_coef_index[:100]])

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

text = data['Groserias'].values 

wordcloud = WordCloud().generate(str(text))

plt.imshow(wordcloud)
plt.axis("off")
plt.show()