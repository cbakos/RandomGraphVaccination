from typing import List

import numpy as np


def create_community_random_color_map(communities: np.array, seed: int = 0) -> np.array:
    """
    Assigns a random color to each node, such that nodes within one community have the same color.
    :param seed:
    :param communities: 1d array of integers, ith value indicates the community id of the ith node
    :return: color_map: a list of colors
    """
    np.random.seed(seed)
    n = communities.shape[0]
    color_list = [np.random.rand(3, ) for _ in range(n)]
    community_cmap = np.array([color_list[i] for i in communities])
    return community_cmap


def community_map_from_community_sizes(community_sizes: List[int]):
    communities = []
    i = 0
    for size in community_sizes:
        for j in range(size):
            communities.append(i)
        i += 1
    return np.array(communities)


def community_sizes_generator(n: int, prop_lr_com_size: float = 0.45, prop_com_size: float = 0.04, seed: int = 1):
    """
    Creates a random vector of communities based on number of nodes and average community size.
    Community sizes follow normal distribution with mean the given average and standard deviation
    such that the values are mostly positive.
    For none positive values that might occur the absolute value is taken.
    """
    np.random.seed(seed)
    # First community is low risk and has half of the population
    communities = [int(prop_lr_com_size * n)]
    # The rest
    leftovers = n - int(prop_lr_com_size * n)
    i = 1
    avg_com_size = n * prop_com_size
    while leftovers > 3 * avg_com_size / 2:
        communities.append(int(abs(np.random.normal(avg_com_size, avg_com_size / 3, 1))))
        leftovers -= communities[i]
        i += 1
    communities.append(leftovers)
    return communities


def correct_deg_sum_to_be_even(seq: np.array):
    # make sure degrees sum to an even number
    if np.sum(seq) % 2 != 0:
        seq[0] += 1
    return seq


def init_infected(n: int, prop_lr_com_size: float,
                  prop_int_inf: float, prop_int_inf_hr: float = 0.5):
    """
    :param n: size of population
    :param prop_lr_com_size: proportion of nodes in the low risk community
    :param prop_int_inf: proportion of initially infected nodes
    :param prop_int_inf_hr: proportion of high risk in the initially infected nodes
    :return: infected: a tuple including the nodes that are infected at the start
    of the simulation
    """
    infected = []
    # n_infected_lr = 0
    # n_infected_hr = 0
    for i in range(n):
        if i < int(prop_lr_com_size * n) and np.random.binomial(1, prop_int_inf * (1 - prop_int_inf_hr)) == 1:
            infected += [i]
            # n_infected_lr+=1
        elif np.random.binomial(1, prop_int_inf * prop_int_inf_hr) == 1:
            infected += [i]
            # n_infected_hr+=1
    return infected
