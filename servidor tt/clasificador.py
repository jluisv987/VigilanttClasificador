from nlpUtilidades import clean_text
import warnings
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


with open('model_pickle','rb') as f:
    clf = pickle.load(f)
with open('vectorizer_pickle','rb') as x:
    tfidf = pickle.load(x)

def clasificarTexto(jsonSolicitud):
    return True    


dato = clean_text("buenos dias, llegando al trabajo")

vec = tfidf.transform([dato])

print(clf.predict(vec))

dato = clean_text("chango hijo de puta imbecil")

vec = tfidf.transform([dato])

print(clf.predict(vec))

dato = clean_text("tu eres basura")

vec = tfidf.transform([dato])

print(clf.predict(vec))
