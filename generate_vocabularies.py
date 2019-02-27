from utils import *
import pickle

'''
    script to generate various dictionnaries
'''

tweet_list = get_tweets(N=1000)
tweet_list_nopunct = get_tweets(N=1000, b_punctuation=False)

fr_stopwords = french_stopwords()

''' punctuation/no stopwords/stemming/no accent'''
[vectorizer1, words_freq1] = build_vectorizer(tweet_list, stopwords=fr_stopwords, b_stemming=True, b_accent=False)

f1 = open("vectorizers/vectorizer1", "w")
pickle.dump(vectorizer1, f1)
f1.close()

#''' no punctuation/no stopwords/stemming/no accent'''
#[vectorizer2, words_freq1] = build_vectorizer(tweet_list_nopunct, stopwords=fr_stopwords, b_stemming=True, b_accent=False)
#f2 = open("vectorizers/vectorizer2", "w")
#pickle.dump(vectorizer2, f2)
#f2.close()
#
#''' punctuation/stopwords/stemming/no accent'''
#[vectorizer3, words_freq3] = build_vectorizer(tweet_list,b_stemming=True, b_accent=False)
#f3 = open("vectorizers/vectorizer3", "w")
#pickle.dump(vectorizer3, f3)
#f3.close()
#
#''' no punctuation/stopwords/stemming/no accent'''
#[vectorizer4, words_freq4] = build_vectorizer(tweet_list_nopunct,b_stemming=True, b_accent=False)
#f4 = open("vectorizers/vectorizer4", "w")
#pickle.dump(vectorizer4, f4)
#f4.close()
#
#''' punctuation/no stopwords/no stemming/no accent'''
#[vectorizer5, words_freq5] = build_vectorizer(tweet_list,stopwords=fr_stopwords, b_accent=False)
#f5 = open("vectorizers/vectorizer5", "w")
#pickle.dump(vectorizer5, f5)
#f5.close()
#
#''' no punctuation/no stopwords/no stemming/no accent'''
#[vectorizer6, words_freq6] = build_vectorizer(tweet_list_nopunct,stopwords=fr_stopwords, b_accent=False)
#f6 = open("vectorizers/vectorizer6", "w")
#pickle.dump(vectorizer6, f6)
#f6.close()
#
#''' punctuation/stopwords/no stemming/no accent'''
#[vectorizer7, words_freq7] = build_vectorizer(tweet_list, b_accent=False)
#f7 = open("vectorizers/vectorizer7", "w")
#pickle.dump(vectorizer7, f7)
#f7.close()
#
#''' no punctuation/stopwords/no stemming/no accent'''
#[vectorizer8, words_freq8] = build_vectorizer(tweet_list_nopunct, b_accent=False)
#f8 = open("vectorizers/vectorizer8", "w")
#pickle.dump(vectorizer8, f8)
#f8.close()
