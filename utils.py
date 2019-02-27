import mysql.connector
from preprocessing import *

def connect_to_db():
    twitter_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="twitter_db"
    )
    return twitter_db

def get_tweets(N=None, b_retweet=False, b_punctuation=True):
    '''
        N : limit
        b_retweet : True if retweets are to be kept
        get (N first) tweets
    '''
    twitter_db = connect_to_db()
    tweet_list = []
    cursor = twitter_db.cursor()

    if N:
        limit = " LIMIT " + str(N)
    else:
        limit = ""

    if b_punctuation:
        text = "text_punct"
    else:
        text = "text"

    if b_retweet:
        query = "SELECT " + text + " FROM tweets WHERE lang='fr'" + limit
    else:
        query = "SELECT " + text + " FROM tweets WHERE NOT (text LIKE '%RT @%') AND lang='fr'" + limit

    cursor.execute(query)

    for text in cursor:
        tweet_list.append(text[0])

    cursor.close()
    return tweet_list

def get_tweets_from_user(user_id, N=None, b_retweet=False):
    '''
        user_id : user id (int)
        N : tweets limit
        b_retweet : True if retweets are to be kept
        get (N first) tweets from user identified by user_id
    '''
    twitter_db = connect_to_db()
    tweet_list = []
    cursor = twitter_db.cursor()

    if N:
        limit = " LIMIT " + str(N)
    else:
        limit = ""

    if b_retweet:
        query = "SELECT text FROM tweets WHERE user_id = " + str(user_id) +" AND lang='fr'" + limit
    else:
        query = "SELECT text FROM tweets WHERE user_id = " + str(user_id) +" AND lang='fr' AND NOT (text LIKE '%RT @%')" + limit

    cursor.execute(query)

    for text in cursor:
        tweet_list.append(text[0])

    cursor.close()
    return tweet_list

def build_vectorizer_from_tweets(N=None, b_retweet=False, stopwords=None, b_stemming=False, b_lowercase=True,b_punctuation=False, b_accent=True, max_f=None):
    '''
        N : tweets limit
        b_retweet : True if retweets are to be kept
        stopwords : list of stopwords (None if stopwords are to be kept)
        b_stemming : boolean indicating whether to stem words
        b_lowercase : boolean indicating whether to lowercase words
        b_punctuation : boolean indicating whether to keep punctuation
        b_accent : boolean indicating whether to keep accents
        max_f : maximum number of top occurring tokens to select
        build and return a vectorizer given the above parameter
            along with a list of tuples containing the words and
            their occurrences in the tweets
    '''
    if b_punctuation:
        tweets = get_tweets(N, b_retweet=b_retweet)
    else:
        tweets = get_tweets(N, b_retweet=b_retweet, b_punctuation=False)

    [vectorizer, words_freq] = build_vectorizer(tweets, stopwords=stopwords, b_stemming=b_stemming, b_lowercase=b_lowercase, b_accent=b_accent, max_f=max_f)
    return vectorizer, words_freq





