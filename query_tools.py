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

def get_tweets_candidates_from_users(users, N=None):
    '''
        return a list of tweets from specified users,
            along with a list of mentioned candidates, for each tweet
    '''
    twitter_db = connect_to_db()
    cursor = twitter_db.cursor()

    if N:
        limit = " LIMIT " + str(N)
    else:
        limit = ""

    query = "SELECT text, candidates\
            FROM tweets\
            WHERE lang='fr' AND \
            (user_id IN " + str(users) + " OR \
            in_reply_to_user_id IN " + str(users) + " OR \
            quoted_user_id IN " + str(users) + " OR \
            retweeted_user_id IN " + str(users) + ")" + limit

    cursor.execute(query)

    tweets = []
    candidates = []
    for tweet, cand in cursor:
        tweets.append(tweet)
        candidates.append(list(cand)) # string of 0 and 1 -> list of 0 and 1
    cursor.close()

    # cast to int
    candidates = np.array(candidates).astype(int)
    return tweets, candidates

def get_nb_tweets_per_user(users_list):
    '''
        users_list : list of user id
        return a dictionary where each key is a user_id
            and its corresponding value, the number of tweets he/she tweeted
    '''
    nb_tweets_per_user = dict()
    twitter_db = connect_to_db()
    for user in users_list:
        cursor = twitter_db.cursor()
        query = "SELECT COUNT(*) FROM tweets WHERE user_id = " + str(user)
        cursor.execute(query)
        nb_tweets_per_user[user] = cursor.fetchall()[0][0]
        cursor.close()
    return nb_tweets_per_user
