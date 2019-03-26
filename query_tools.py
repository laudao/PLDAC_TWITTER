import mysql.connector
import numpy as np

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
    return np.array(tweet_list)

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
    return np.array(tweet_list)


