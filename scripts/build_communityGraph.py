import sys
sys.path.insert(0, '../src')
from utils import *
import pandas as pd
from collections import Counter
import pickle

N = 10000

################################################################
####    Generate community graph from a sample of N tweets   ###
###############################################################

twitter_db = connect_to_db()
cursor = twitter_db.cursor()

# get users involved in N first tweets
query = ("SELECT t1.user_id, t1.in_reply_to_user_id, t1.quoted_user_id, t1.retweeted_user_id \
        FROM tweets t1\
        WHERE lang='fr' AND \
        ((NOT (t1.text LIKE '%RT @%')) OR \
        (t1.text LIKE '%RT @%' AND \
            EXISTS \
                (SELECT * \
                FROM tweets t2 \
                WHERE t2.user_id = t1.user_id AND NOT (t2.text LIKE '%RT @%')\
                )\
        )\
        )\
        LIMIT " + str(N))

cursor.execute(query)
print("Executed query")

# create a dictionary from these tweets
# where each key is a user id
# and each value is a dictionary containing ids of users whom he/she replied to/quoted/retweeted
G_dict = dict()

for (user_id, in_reply_to_user_id, quoted_user_id, retweeted_user_id) in cursor:
    if user_id not in G_dict:
        G_dict[user_id] = {'replied_to': {}, 'quoted': {}, 'retweeted': {}}

    if not(in_reply_to_user_id is None):
        if in_reply_to_user_id not in G_dict:
            G_dict[in_reply_to_user_id] = {'replied_to': {}, 'quoted': {}, 'retweeted': {}}
        if in_reply_to_user_id not in G_dict[user_id]['replied_to']:
            G_dict[user_id]['replied_to'][in_reply_to_user_id] = 1
        else:
            G_dict[user_id]['replied_to'][in_reply_to_user_id] += 1

    if not(quoted_user_id is None):
        if quoted_user_id not in G_dict:
            G_dict[quoted_user_id] = {'replied_to': {}, 'quoted': {}, 'retweeted': {}}
        if quoted_user_id not in G_dict[user_id]['quoted']:
            G_dict[user_id]['quoted'][quoted_user_id] = 1
        else:
            G_dict[user_id]['quoted'][quoted_user_id] += 1

    if not(retweeted_user_id is None):
        if retweeted_user_id not in G_dict:
            G_dict[retweeted_user_id] = {'replied_to': {}, 'quoted': {}, 'retweeted': {}}
        if retweeted_user_id not in G_dict[user_id]['retweeted']:
            G_dict[user_id]['retweeted'][retweeted_user_id] = 1
        else:
            G_dict[user_id]['retweeted'][retweeted_user_id] += 1

cursor.close()
print("Created dictionary")

# create the corresponding networkx.DiGraph
G = nx.DiGraph()
G.add_nodes_from(G_dict.keys())

for (u1,v) in G_dict.items():
    for (u2, count) in v['quoted'].items():
        G.add_edge(u1,u2,label='quoted',weight=count)
    for (u2, count) in v['replied_to'].items():
        G.add_edge(u1,u2,label='replied_to',weight=count)
    for (u2, count) in v['retweeted'].items():
        G.add_edge(u1,u2,label='retweeted',weight=count)

print("Created graph")

i = 1
# save graph to file
f = open("../communities/v" + str(i) + "/graph", "wb")
pickle.dump(G,f)
f.close()

print("Saved graph to file communities/v" + str(i) + "/graph")

G_undirected = nx.Graph(G)

partition = community_louvain.best_partition(G_undirected)
print("Computed partition")
pos = community_layout(G_undirected, partition)
print("Computed community layout")

# save partition to file
f = open("../communities/v" + str(i) + "/partition", "wb")
pickle.dump(partition,f)
f.close()

print("Saved partition to file communities/" + str(i) + "/partition")

# save graph layout to file
f = open("../communities/v" + str(i) + "/layout", "wb")
pickle.dump(pos,f)
f.close()

print("Saved graph layout to file communities/" + str(i) + "/layout")

# to adjust node size according to corresponding user's number of tweets
all_users = list(partition.keys())
nb_tweets_per_user = get_nb_tweets_per_user(all_users)

f = open("../communities/v" + str(i) + "/nb_tweets_per_user", "wb")
pickle.dump(nb_tweets_per_user,f)
f.close()

print("Saved number of tweets per user to file communities/v" + str(i) + "/nb_tweets_per_user")

