import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt
import numpy as np
from query_tools import *

def filter_graph_community(partition, G, node_size, filter_community):
    partition_filtered = dict()
    G_filtered = G.copy()
    filtered_node_size = dict()
    for user_id, comm_id in partition.items():
        if comm_id in filter_community:
            partition_filtered[user_id] = comm_id
            filtered_node_size[user_id] = node_size[user_id]
        else:
            G_filtered.remove_node(user_id)

    return partition_filtered, G_filtered, filtered_node_size

def filter_graph_users(partition, G, node_size, filter_users):
    partition_filtered = dict()
    G_filtered = G.copy()
    filtered_node_size = dict()
    for user_id, comm_id in partition.items():
        if user_id in filter_users:
            partition_filtered[user_id] = comm_id
            filtered_node_size[user_id] = node_size[user_id]
        else:
            G_filtered.remove_node(user_id)

    return partition_filtered, G_filtered, filtered_node_size

def save_hist(data, filename, fig_size=12):
    plt.figure(figsize=(fig_size, fig_size))
    h = plt.hist(data)
    plt.savefig(filename)

def plot_community_graph(G, layout, partition, dict_node_size, fig_size=12, dict_node_color=None, filename=None):
    '''
        G : community graph to plot
        layout : graph layout
        partition : dictionary mapping each node to its community
        dict_node_size : dictionary mapping each node to its size
        fig_size : figure size, default=12
        filename : save plot to filename if not None
        plot community graph
    '''
    _node_size = np.log(np.array([dict_node_size.get(node) for node in G.nodes()]))

    if dict_node_color is None:
        _node_color=[partition.get(node) for node in G.nodes()]
    else:
        _node_color=[dict_node_color.get(node) for node in G.nodes()]

    plt.figure(figsize=(fig_size, fig_size))
    nx.draw_networkx_nodes(G, layout, node_size=_node_size, \
        node_color=_node_color)
    nx.draw_networkx_edges(G, layout, alpha=0.3)
    plt.axis('off')

    if not filename is None:
        plt.savefig(filename)

def get_nodes_color(nodes):
    '''
        nodes : array of users id
        return dictionary mapping each user in nodes to its color,
            base on which candidate he mentions the most
    '''
    candidates_color_mapping = {
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
    dict_nodes_color = dict()
    for u in nodes:
        candidates = mentioned_candidates_from_user(u, N=50)
        dict_nodes_color[u] = candidates_color_mapping[np.argmax(np.sum(candidates, axis=0))]

    return dict_nodes_color

'''
    code below is taken from Paul Brodersen's implementation, posted on Stackoverflow
'''

def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos

def _position_communities(g, partition, **kwargs):

    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos

def _find_between_community_edges(g, partition):

    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges

def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos

