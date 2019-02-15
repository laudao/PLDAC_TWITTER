import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import string
import unicodedata

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

def merge_tokens(token):
    token_ = remove_accents(token.lower())
    if token_ in ["jlm", "melenchon", "jean-luc"]:
        return "melenchon"
    if token_ in ["emmanuel", "macron"]:
        return "macron"
    if token_ in ["marine", "marinelepen", "lepen"]:
        return "marine"
    if token_ in ["fillon", "françois", "francois"]:
        return "fillon"
    return token

def clean_doc(s):
    s = s.split(" ")
    clean_s = []
    for token in s:
        token = merge_tokens(token)
        token=token.replace('#','')
        if "'" in token:
            token = token.split("'",1)[1]
        if not ((len(token)<=4 and "'" in token) or "@" in token or "http" in token or len(token) <= 2):
            clean_s.append(token)
    clean_s = ' '.join(clean_s)
    return clean_s


def build_vectorizer(docs, stopwords=None, b_stemming=False, b_lowercase=True,b_punctuation=False, b_accent=True, max_f=None):
    '''
        docs : list of documents
        stopwords : list of stopwords (None if stopwords are to be kept)
        b_stemming : boolean indicating whether to stem words
        b_lowercase : boolean indicating whether to lowercase words
        b_punctuation : boolean indicating whether to keep punctuation
        b_accent : boolean indicating whether to keep accents
        max_f : maximum number of top occurring tokens to select
        build and return a vectorizer given the above parameter
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
        token_pattern_ = r'(?u)\b\w\w+\b|!|\?'
    if not b_accent:
        print("Removing accents")

        if not (stopwords is None):
            stopwords = [remove_accents(w) for w in stopwords]


    if not (max_f is None):
        print("Keeping the top {} occurring tokens".format(max_f))

    vectorizer = CountVectorizer(preprocessor=clean_doc, stop_words=stopwords, tokenizer=tokenizer_, lowercase=lower, token_pattern=token_pattern_, max_features=max_f)
    X = vectorizer.fit_transform(docs)

    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)

    return vectorizer, words_freq

def vectorize_docs(vectorizer, docs):
    '''
        features : vectorizer built beforehand
        docs : documents to vectorize
        given a vectorizer, vectorize documents
    '''
    X = vectorizer.transform(docs)
    return X.toarray()

def cos_sim(a,b):
    '''
        a,b : vectors
        compute cosine similarity between a and b
    '''
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
