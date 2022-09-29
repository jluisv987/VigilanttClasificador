import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import re
import es_core_news_md
import unidecode
import unicodedata

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
