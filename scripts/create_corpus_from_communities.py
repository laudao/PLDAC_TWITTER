import sys
sys.path.insert(0, '../src')
from utils import *
import pickle
import matplotlib.pyplot as plt

"""
    This script consists of :
    - cleaning each community i.e. remove users that only retweet or do not sufficiently
      to the community (in terms of centrality degree)
    - for each community, retrieving users' tweets in order to create a representative
      corpus of positive tweets regarding said candidate/negative tweets regarding the
      others
    - saving candidate -> users and candidate -> tweets mappings to files
    - if sys.argv[1] = 1, plotting each community and save it to its respective file
"""

plot_graphs = False

if len(sys.argv) > 1 and sys.argv[1] == '1':
    plot_graphs = True

candidates_mapping = {
    0 : "Arthaud",
    1 : "Asselineau",
    2 : "Cheminade",
    3 : "Dupont-Aignan",
    4 : "Fillon",
    5 : "Hamon",
    6 : "Lassalle",
    7 : "Le Pen",
    8 : "Macron",
    9 : "Mélenchon",
    10 : "Poutou"
}

candidate_color_mapping = {
    0 : "#f58231", # Arthaud -> orange
    1 : "#808000", # Asselineau -> olive
    2 : "#9A6324", # Cheminade -> brown
    3 : "#800000", # Dupont-Aignan -> maroon
    4 : "green", # Fillon
    5 : "yellow", # Hamon
    6 : "magenta", # Lassalle
    7 : "#000075", # Le Pen -> navy
    8 : "blue", # Macron
    9 : "red", # Mélenchon
    10 : "purple" # Poutou
}

version = 1

f = open("../communities/v" + str(version) + "/partition", "rb")
partition = pickle.load(f)
f.close()

f = open("../communities/v" + str(version) + "/nb_tweets_per_user", "rb")
nb_tweets_per_user = pickle.load(f)
f.close()

f = open("../communities/v" + str(version) + "/graph", "rb")
G = pickle.load(f)
f.close()

f = open("../communities/v" + str(version) + "/candidate_to_community", "rb")
candidate_to_community = pickle.load(f)
f.close()

# dictionary mapping each candidate to the users that support them
candidate_to_users = dict()

# remove users that only retweet
for cand, community in candidate_to_community.items():
    users = community[:,0]
    nb_retweets_per_user = get_ratio_retweets_per_user(users)
    nb_retweets_per_user = np.array([(user, ratio) for user, ratio in nb_retweets_per_user.items()])
    to_keep = nb_retweets_per_user[np.where(nb_retweets_per_user[:,1] < 1)][:,0]
    candidate_to_users[cand] = to_keep
    print("{} - number of bots among {} users : {}".format(candidates_mapping[cand], len(users),\
                                                           len(users) - len(to_keep)))

# dictionary mapping each candidate to their representative tweets
corpus = dict()

for cand, users in candidate_to_users.items():
    print(cand)
    fname = "../communities/v" + str(version) + "/plot_community_" + candidates_mapping[cand]
    partition_cand, G_cand, nb_tweets_cand = filter_graph_users(partition, \
            G, nb_tweets_per_user, users)

    dict_centrality = nx.degree_centrality(G_cand)
    # set threshold to eliminate users that do not sufficiently belong to the community
    dict_centrality_filtered = {k:v for k,v in dict_centrality.items() if v > 0.005}
    users_to_keep = list(dict_centrality_filtered.keys())

    # update community
    candidate_to_users[cand] = users_to_keep

    if plot_graphs:
        users_color = get_nodes_color(users_to_keep)

        partition_cand, G_cand, nb_tweets_cand = filter_graph_users(partition, \
                G, nb_tweets_per_user, users_to_keep)
        pos_cand = community_layout(G_cand, partition_cand)
        # save plot
        plot_community_graph(G_cand, pos_cand, partition_cand, nb_tweets_cand, \
                dict_node_color=users_color, filename=fname)

    # get 10 tweets from each user
    tweets = []
    for user in users_to_keep:
        tweets = np.append(tweets, get_tweets_from_user(user, N=10))
    corpus[cand] = tweets

    print("Computed corpus for {}".format(candidates_mapping[cand]))

# save updated candidate -> users mapping to file
f = open("../communities/v" + str(version) + "/candidate_to_users", "wb")
pickle.dump(candidate_to_users,f)
f.close()

print("Saved dictionary mapping candidates to their representative users in file communities/v" \
        + str(version) + "/candidate_to_users")

# save candidate -> tweets to file
f = open("../communities/v" + str(version) + "/candidate_to_tweets", "wb")
pickle.dump(corpus,f)
f.close()

print("Saved dictionary mapping candidates to their tweets in file communities/v" \
        + str(version) + "/candidate_to_tweets")


