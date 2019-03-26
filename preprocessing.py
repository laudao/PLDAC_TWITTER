import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import string
import unicodedata
import re

punctuation_dict = {'!': 'single_exl', '!!': 'mult_exl', '?': 'single_int',\
                    '??': 'mult_int', '...': 'susp_pts', '…': 'susp_pts',\
                    '?!.': 'mixed_m'}

def french_stopwords():
    fr_stopwords = nltk.corpus.stopwords.words('french')
    fr_stopwords.extend(['de', 'ou', 'sur', 'or', 'ni', 'car', 'quand', 'a', 'mais', 'donc', 'si', 'quel', 'entre', 'tout', 'ce', 'cet', 'ça', 'tous', "c'est", 'faire', 'dans', 'fait'])
    return fr_stopwords

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
    if token_ in ["jlm", "melenchon", "jean-luc", "jlmelenchon"]:
        return "melenchon"
    if token_ in ["emmanuel", "macron", "emmanuelmacron"]:
        return "macron"
    if token_ in ["marine", "marinelepen", "lepen"]:
        return "marine"
    if token_ in ["fillon"]:
        return "fillon"
    if token_ in ["benoit", "benoithamon", "hamon", "benoît"]:
        return "hamon"
    return token

def format_punctuation(s):
    formatted_s = re.sub(r"(?<!\!|\?|\.)[\!](?!\!|\?|\.)"," single_excl ", s)
    formatted_s = re.sub(r"(?<!\?|\.)[\!]+(?!\?|\.)", " mult_excl ", formatted_s)
    formatted_s = re.sub(r"(?<!\!|\?|\.)[\?](?!\!|\?|\.)", " single_int ", formatted_s)
    formatted_s = re.sub(r"(?<!\!|\.)[\?]+(?!\!|\.)", " mult_int ", formatted_s)
    formatted_s = re.sub(r"(?<!\w)[\.\.]+(?!\w)", " susp_pts ", formatted_s)
    formatted_s = re.sub(r"(?<!\w)[\.|\?|\!]+(?!\w)", " mixed_m ", formatted_s)
    return formatted_s

def clean_doc_lower(s):
    '''
        s : document as a string
        preprocess s - lowercasing included
    '''
    s = s.split(" ")
    clean_s = []
    for token in s:
        token = token.lower()
        token=token.replace('#','')
        token=token.replace('@', '')
        token = merge_tokens(token)
        if "'" in token:
            token = token.split("'",1)[1]
        if not ((len(token)<=4 and "'" in token) or "http" in token or len(token) <= 2):
            clean_s.append(token)
    clean_s = ' '.join(clean_s)
    return clean_s

def clean_doc_no_lower(s):
    '''
        s : document as a string
        preprocess s while keeping uppercase
    '''
    s = s.split(" ")
    clean_s = []
    for token in s:
        token=token.replace('#','')
        token=token.replace('@', '')
        token = merge_tokens(token)
        if "'" in token:
            token = token.split("'",1)[1]
        if not ((len(token)<=4 and "'" in token) or "http" in token or len(token) <= 2):
            clean_s.append(token)
    clean_s = ' '.join(clean_s)
    return clean_s

def stem_words(doc):
    '''
        doc : document (string)
        stem words in doc
    '''
    stemmer = SnowballStemmer('french')
    tokenizer = CountVectorizer().build_tokenizer()
    return (stemmer.stem(w) for w in tokenizer(doc))


def build_vectorizer(docs, stopwords=None, b_stemming=False, b_lowercase=False, b_rmaccent=False, max_f=None):
    '''
        docs : list of documents
        stopwords : list of stopwords (None if stopwords are to be kept)
        b_stemming : boolean indicating whether to stem words (default:False)
        b_lowercase : boolean indicating whether to lowercase words (default:False)
        b_rmaccent : boolean indicating whether to remove accents (default:False)
        max_f : maximum number of top occurring tokens to select
        build and return a vectorizer given the above parameters
            along with the document-term matrix representation of the tweets
    '''
    tokenizer_ = None
    lower = True
    preprocessor_ = clean_doc_no_lower

    if not (stopwords is None):
        print("Removing stopwords")

    if b_stemming:
        print("Stemming")
        stemmer = SnowballStemmer('french')

        #def stemmed_words(doc):
        #    return (stemmer.stem(w) for w in tokenizer(doc))

        tokenizer_ = stem_words

        if not (stopwords is None):
            stemmed_stopwords = [stemmer.stem(t) for t in stopwords]
            stopwords = stemmed_stopwords
    if b_lowercase:
        print("Removing uppercases")
        preprocessor_ = clean_doc_lower
    if b_rmaccent:
        print("Removing accents")

        if not (stopwords is None):
            stopwords = [remove_accents(w) for w in stopwords]

    if not (max_f is None):
        print("Keeping the top {} occurring tokens".format(max_f))

    vectorizer = CountVectorizer(preprocessor=preprocessor_, stop_words=stopwords, tokenizer=tokenizer_, max_features=max_f)
    X = vectorizer.fit_transform(docs)

    return vectorizer, X

def get_words_freq(vectorizer, X):
    '''
        vectorizer : CountVectorizer
        X : document-term matrix
        return a list of tuples containing the words of the vocabulary
            and their occurrences in the tweets,
            sorted by occurrence
    '''
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)

    return words_freq

def vectorize_docs(vectorizer, docs):
    '''
        features : vectorizer built beforehand
        docs : documents to vectorize
        given a vectorizer, vectorize documents
    '''
    X = vectorizer.transform(docs)
    return X

def cos_sim(a,b):
    '''
        a,b : vectors
        compute cosine similarity between a and b
    '''
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
