from utils import *

'''
    cand1 : Nathalie Arthaud
    cand2 : François Asselineau
    cand3 : Jacques Cheminade
    cand4 : Nicolas Dupont-Aignan
    cand5 : François Fillon
    cand6 : Benoît Hamon
    cand7 : Jean Lassalle
    cand8 : Marine Le Pen
    cand9 : Emmanuel Macron
    cand10 : Jean-Luc Mélenchon
    cand11 : Philippe Poutou
'''

twitter_db = connect_to_db()
cursor = twitter_db.cursor()
### les colonnes ont été préalablement créées
query = "SELECT text, tweet_id FROM tweets WHERE lang='fr'"
cursor.execute(query)

for (text, tweet_id) in cursor.fetchall():
    cursor2 = twitter_db.cursor()

    if re.findall(r"\b(le pen|lepen|marine)\b",text,re.IGNORECASE):
        sql = """ UPDATE tweets SET cand8 = 1 WHERE tweet_id = %s"""
        val = tweet_id
        cursor2.execute(sql, val)
    if re.match(r"\b(emmanuel|macron)\b",text,re.IGNORECASE):
        sql = """ UPDATE tweets SET cand9 = 1 WHERE tweet_id = %s"""
        val = tweet_id
        cursor2.execute(sql, val)

    '''
        à compléter avec les autres candidats
    '''

    print(tweet_id)
    cursor2.close()
    twitter_db.commit()

print("{} record(s) affected".format(cursor.rowcount))
cursor.close()
twitter_db.close()



