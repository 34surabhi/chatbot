from DBconnection import get_training_data
import pandas as pd
import numpy as np
import re
import spacy
import nltk
import sklearn
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

df = get_training_data()

#print(df.head())

#Assigning new column names
df.columns = ['id', 'text', 'category', 'tags', 'keywords']

df = df.drop(columns=['id'])  # Drop any column you don’t need

#print(df.columns)

#print(df.info())
#Check the total number of missing rows in the dataset
#print(df.isnull().sum())

#Drop null rows
df = df.dropna()

#print(df.isnull().sum())
#df[df['complaint_what_happened']==''] = np.nan
df = df.replace(['', 'NA', 'N/A', 'na', 'null', 'NULL', '-', '--'], np.nan)
#print(df.isna().sum())  # count of missing values per column

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)                     # Remove [brackets]
    text = re.sub(r'[^\w\s]', '', text)                     # Remove punctuation
    text = re.sub(r'\w*\d\w*', '', text)                    # Remove alphanumeric words
    text = re.sub(r'\s+', ' ', text).strip()                # Normalize spaces
    return text

def lemmatize_text(text):
    doc = nlp(text)
    lemmas = [
        token.lemma_ for token in doc
        if token.lemma_ not in stop_words
        and token.lemma_ != '-PRON-'
        and token.is_alpha
    ]
    return " ".join(lemmas)

df['cleaned_text'] = df['text'].apply(clean_text)
df['lemmatized_text'] = df['cleaned_text'].apply(lemmatize_text)

#print(df[['text', 'cleaned_text', 'lemmatized_text', 'category']].head())

X = df['lemmatized_text']
y = df['category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tfidf = TfidfVectorizer(max_features=3000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))




