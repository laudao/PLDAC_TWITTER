import mysql.connector
import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import string
import unicodedata

def connect_to_db():
    twitter_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="twitter_db"
    )
    return twitter_db

def remove_punctuation(doc):
    return ''.join([char for char in doc if char not in string.punctuation])

def remove_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def build_vectorizer(docs, stopwords=None, b_stemming=False, b_lowercase=True     ,b_punctuation=False, b_accent=True):
    '''
        docs : list of documents
        stopwords : list of stopwords (None if stopwords are to be kept)
        b_stemming : boolean indicating whether to stem words
        b_lowercase : boolean indicating whether to lowercase words
        b_punctuation : boolean indicating whether to keep punctuation
        b_accent : boolean indicating whether to keep accents
        define and return a vectorizer given the above parameter
            along with a list of tuples containing the words and
            their occurrences in the docs
    '''
    tokenizer_ = None
    lower = True
    token_pattern_ = r'(?u)\b\w\w+\b'

    if b_stemming:
        print("Stemming")
        stemmer = SnowballStemmer('french')
        tokenizer = CountVectorizer().build_tokenizer()

        def stemmed_words(doc):
            return (stemmer.stem(w) for w in tokenizer(doc))

        tokenizer_ = stemmed_words

        if not (stopwords is None):
            stemmed_stopwords = [stemmer.stem(t) for t in stopwords]
            stopwords = stemmed_stopwords
    if not b_lowercase:
        print("Keeping uppercase")
        lower = False
    if b_punctuation:
        print("Keeping punctuation")
        token_pattern_ = r"(?u)\b\w\w+\b|!|\?|\"|\'"
    if not b_accent:
        print("Removing accents")

        if not (stopwords is None):
            stopwords = [remove_accents(w) for w in stopwords]

    def clean_doc(s):
        s = s.replace('#', '')

        if not b_accent:
            s = remove_accents(s)
        if "'" in s:
            s = s.split("'",1)[1]
        if not ((len(s)<=4 and "'" in s) or "@" in s or "http" in s or len(s) <= 2):
            return s
        return ""

    vectorizer = CountVectorizer(preprocessor=clean_doc, stop_words=stopwords, tokenizer=tokenizer_, lowercase=lower, token_pattern=token_pattern_)
    X = vectorizer.fit_transform(docs)

    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)

    return vectorizer, words_freq

def vectorize_docs(vectorizer, docs):
    return vectorizer.transform(docs)



