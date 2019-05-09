import sys
sys.path.insert(0, '../src')
from utils import *
import pickle
import matplotlib.pyplot as plt
from collections import Counter

####################################################################################
####    Link each community with at least more than 100 nodes to its candidate   ###
###################################################################################
version = 1

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

f = open("../communities/v" + str(version) + "/partition", "rb")
partition = pickle.load(f)
f.close()

f = open("../communities/v" + str(version) + "/nb_tweets_per_user", "rb")
nb_tweets_per_user = pickle.load(f)
f.close()
f = open("../communities/v" + str(version) + "/graph", "rb")
G = pickle.load(f)
f.close()

values = list(partition.values())
# for each community, count number of users belonging to it
c = Counter(values)
# sort communities in descending order with respect to their number of users
communities_id_sorted = sorted(np.unique(values), key=c.get, reverse=True)

# create array where first column = community, second column = size of community
communities_counts = [(community_id, c[community_id]) for community_id in communities_id_sorted]
communities_counts = np.array(communities_counts)

# keep communities that contain more than 100 nodes
communities_filtered = communities_counts[np.where(communities_counts[:,1] >= 100)][:,0]
k = len(communities_filtered)

print("Keeping the following communities : {}".format(communities_filtered))

# remove parts of the graph that are unrelated to these communities
partition_filtered, G_filtered, nb_tweets_per_user_filtered = filter_graph_community\
                                                    (partition, G, \
                                                    nb_tweets_per_user,\
                                                    communities_filtered)

print("Built new graph based on these communities")

# compute new graph layout
pos = community_layout(G_filtered, partition_filtered)

print("Computed new graph layout based on these communities")

plot_community_graph(G_filtered, pos, partition_filtered, nb_tweets_per_user_filtered,\
        filename="../communities/v" + str(version) + "/plot_biggest_communities")

# create array out of partition_filtered
partition_filtered_array = np.array([(user_id, community) for (user_id, community) in partition_filtered.items()])

# create array out of nb_tweets_per_user
nb_tweets_filtered_array = np.array([(user_id, nb) for (user_id, nb) in nb_tweets_per_user_filtered.items()])

# element i of communities is the subarray of partition_filtered_array corresponding to the ith biggest community
communities = []
for i in range(k):
    com = partition_filtered_array[np.where\
            (partition_filtered_array[:,1] == communities_filtered[i])]
    communities.append(com)

# dictionary mapping (if possible) each candidate to its community
# some candidates are likely to be left with no community, if not mentioned enough times
candidate_to_community = dict()
# 0 if candidate is not mapped to its community, 1 elsewise
mapped = np.zeros(11)

for i in range(k):
    # get users from ith biggest community
    users = communities[i][:,0]
    # compute average number of tweets among this community
    avg = np.mean(nb_tweets_filtered_array[np.where(np.in1d(nb_tweets_filtered_array[:,0],\
            users))][:,1])
    candidates = mentioned_candidates_from_mult_users(tuple(users),10000,keep_retweets=True)
    cand = np.argmax(np.sum(candidates, axis=0))

    if mapped[cand] == 0:
        candidates_to_community[cand] = communities[i]
        mapped[cand] = 1

    print("Community {} - average number of tweets per user : {} - \
            most mentioned candidate : {}".format(communities_filtered[i], \
            avg, candidates_mapping[cand]))

for k,v in candidate_to_community.items():
    print("{} -> community {}".format(candidates_mapping[k], v[0][1]))


# save mapping to file
f = open("../communities/v" + str(version) + "/candidate_to_community", "wb")
pickle.dump(candidates_to_community,f)
f.close()

print("Saved dictionary mapping candidates to their community in file communities/v" \
        + str(version) + "/candidates_to_community")

