import numpy as np
import networkx as nx


def create_half_edges_between_communities(deg_seq_out, communities):
    # make list of n empty lists where n the number of communities
    half_edges = [[] for _ in range(len(np.unique(communities)))]

    # setup half edge map
    for v_index in range(len(deg_seq_out)):  # for all nodes
        for h in range(deg_seq_out[v_index]):  # for all half_edges of node
            half_edges[int(communities[v_index])].append(v_index)  # add node to list of its community
    return half_edges


def is_community_structure_possible(deg_seq_out, communities):
    # for each community the number of out h.e.-s cannot exceed the total number of h.e.-s from every other community
    # half_edges = create_half_edges_between_communities(deg_seq_out=deg_seq_out, communities=communities)
    community_ids = np.unique(communities)
    for c in community_ids:
        vertex_ids_in_c = np.where(communities == c)[0]
        vertex_ids_not_in_c = np.where(communities != c)[0]
        assert np.sum(deg_seq_out[vertex_ids_in_c.astype(int)]) <= np.sum(deg_seq_out[vertex_ids_not_in_c.astype(int)]), \
            "for each community the number of out h.e.-s cannot exceed the total number of h.e.-s from every other " \
            "community"


def cm_for_communities(deg_seq_in: np.array,
                       communities: np.array,
                       graph: nx.Graph,
                       community_for_general_pop=True,
                       seed=0):
    community_ids = np.unique(communities)
    # if general population is not a community, then don't create edges between community 0 nodes
    if not community_for_general_pop:
        community_ids = community_ids[1:]
        # add community zero nodes without edges:
        vertex_ids_for_0 = np.where(communities == 0)[0]
        graph.add_nodes_from(vertex_ids_for_0)

    # Run configuration model for each community, use degree sequence meant for within communities
    for c in community_ids:
        # get vertex ids for current community
        vertex_ids_for_c = np.where(communities == c)[0]  # index 0 since we have only one dimension
        # call nx.Graph to get a (non-erased) Configuration Model Multigraph
        community_sub_graph = nx.configuration_model(deg_sequence=deg_seq_in[vertex_ids_for_c], seed=seed)
        community_sub_graph.remove_edges_from(nx.selfloop_edges(community_sub_graph))  # remove self loops
        # Remove Parallel Edges by turning the Multigraph into a Graph
        community_sub_graph = nx.Graph(community_sub_graph)
        graph = nx.disjoint_union(graph, community_sub_graph)
    return graph


def get_half_edges(deg_seq_in: np.array, deg_seq_out: np.array, communities: np.array):
    general_pop_nodes = np.where(communities == 0)[0]  # general population nodes
    community_nodes = np.nonzero(communities)[0]  # community nodes
    half_edges = []
    for g_node_id in general_pop_nodes:
        for _ in range(deg_seq_in[g_node_id]):
            half_edges.append(g_node_id)
        for _ in range(deg_seq_out[g_node_id]):
            half_edges.append(g_node_id)
    for g_node_id in community_nodes:
        for _ in range(deg_seq_out[g_node_id]):
            half_edges.append(g_node_id)
    return half_edges


