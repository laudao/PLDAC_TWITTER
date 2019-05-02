from preprocessing import *
from query_tools import *
from parsing import *
from community_graph import *

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
        get the N first tweets in the database,
            build and return a vectorizer given the above parameters
            along with a list of tuples containing the words and
            their occurrences in the tweets
    '''
    if b_punctuation:
        tweets = get_tweets(N, b_retweet=b_retweet)
    else:
        tweets = get_tweets(N, b_retweet=b_retweet, b_punctuation=False)

    [vectorizer, words_freq] = build_vectorizer(tweets, stopwords=stopwords, b_stemming=b_stemming, b_lowercase=b_lowercase, b_accent=b_accent, max_f=max_f)
    return vectorizer, words_freq

def get_ratio_retweets_per_user(users_list):
    ratio_per_user = dict()
    nb_tweets_per_user = get_nb_tweets_per_user(users_list)
    nb_retweets_per_user = get_nb_retweets_per_user(users_list)

    for user, nb in nb_tweets_per_user.items():
        if nb > 0:
            ratio_per_user[user] = nb_retweets_per_user[user] * 1.0 / nb

    return ratio_per_user




