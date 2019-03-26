from utils import *
import pickle

'''
    script to save various CountVectorizers, along with their associated word frequencies
'''

tweet_list = get_tweets(N=1000)
tweet_list_nopunct = get_tweets(N=1000, b_punctuation=False)

fr_stopwords = french_stopwords()

''' punctuation/no stopwords/stemming/no accent'''
[vectorizer1, X1] = build_vectorizer(tweet_list, stopwords=fr_stopwords, b_stemming=True, b_rmaccent=True)

f1 = open("vocs/voc1", "wb")
pickle.dump(vectorizer1, f1)
f1.close()

#''' no punctuation/no stopwords/stemming/no accent'''
#[vectorizer2, words_freq2] = build_vectorizer(tweet_list_nopunct, stopwords=fr_stopwords, b_stemming=True, b_accent=False)
#f2 = open("vocs/voc2", "wb")
#pickle.dump(words_freq2, f2)
#f2.close()
#
#''' punctuation/stopwords/stemming/no accent'''
#[vectorizer3, words_freq3] = build_vectorizer(tweet_list,b_stemming=True, b_accent=False)
#f3 = open("vocs/voc3", "wb")
#pickle.dump(words_freq3, f3)
#f3.close()
#
#''' no punctuation/stopwords/stemming/no accent'''
#[vectorizer4, words_freq4] = build_vectorizer(tweet_list_nopunct,b_stemming=True, b_accent=False)
#f4 = open("vocs/voc4", "wb")
#pickle.dump(words_freq4, f4)
#f4.close()
#
#''' punctuation/no stopwords/no stemming/no accent'''
#[vectorizer5, words_freq5] = build_vectorizer(tweet_list,stopwords=fr_stopwords, b_accent=False)
#f5 = open("vocs/voc5", "wb")
#pickle.dump(words_freq5, f5)
#f5.close()
#
#''' no punctuation/no stopwords/no stemming/no accent'''
#[vectorizer6, words_freq6] = build_vectorizer(tweet_list_nopunct,stopwords=fr_stopwords, b_accent=False)
#f6 = open("vocs/voc6", "wb")
#pickle.dump(words_freq6, f6)
#f6.close()
#
#''' punctuation/stopwords/no stemming/no accent'''
#[vectorizer7, words_freq7] = build_vectorizer(tweet_list, b_accent=False)
#f7 = open("vocs/voc7", "wb")
#pickle.dump(words_freq7, f7)
#f7.close()
#
#''' no punctuation/stopwords/no stemming/no accent'''
#[vectorizer8, words_freq8] = build_vectorizer(tweet_list_nopunct, b_accent=False)
#f8 = open("vocs/voc8", "wb")
#pickle.dump(words_freq8, f8)
#f8.close()
