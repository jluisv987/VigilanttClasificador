
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
import pickle
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings('ignore')
#spacy
stop_words_spacy = list(STOP_WORDS)
data = pd.read_csv('Completo.csv')
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
    
    text = remove_special_characters(text)
    
    text = text_to_lowercase(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    #print(text)

    return text

data["Groserias"] = data["Groserias"].apply(clean_text)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

tfidf = TfidfVectorizer(max_features=5000)
data = shuffle(data)
X = data['Groserias']
y = data['Agresivo']
X = tfidf.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)

clf = LogisticRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test,y_pred))
with open('model_pickle','wb') as f:
    pickle.dump(clf,f)

with open('vectorizer_pickle','wb') as x:
    pickle.dump(tfidf,x)

dato = clean_text("tirar la basura en su lugar es lo correcto")

vec = tfidf.transform([dato])

print(clf.predict(vec))

