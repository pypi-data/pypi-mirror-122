import numpy as np
from math import log2


def get_v(M, vs):
    # intra- and inter- affinity
    # return np.sum(M[vs, :]) - np.sum([M[i, i] for i in vs])
    return np.sum(M[vs, :])


def get_s(M, vs):
    # intra-affinity
    return np.sum(M[np.ix_(vs, vs)])


def get_g(M, vs):
    # inter-affinity
    return get_v(M, vs) - get_s(M, vs)


def get_se(vG, g, V, pV):
    return float(g)/float(vG)*log2(float(pV)/float(V))


def get_se_for_vertices(M, vG, vs, pV):
    g = get_g(M, vs)
    V = get_v(M, vs)
    return get_se(vG, g, V, pV)


def get_se_for_vertex(M, d, vG, bin, pV):
    if get_se(vG, d[bin], d[bin], pV) != get_se_for_vertices(M, vG, [bin], pV):
        raise ValueError("bin se error")
    return get_se_for_vertex(M, vG, [bin], pV)


def get_delta_se_plus(M, vG, d, parent, node1, node2):
    # leaf merge
    new_V = node1.V + node2.V
    new_s = node1.s + node2.s
    new_s_tmp = 0
    for b1 in node1.vs:
        for b2 in node2.vs:
            new_s_tmp += M[b1, b2]
    # new_s_tmp = np.sum(M[np.ix_(node1.vs, node2.vs)])
    new_s += 2*new_s_tmp
    '''
    new_se = ((new_V-new_s)*log2(vG/new_V) + (new_V*log2(new_V)-node1.sum_b_log_b-node2.sum_b_log_b)) / vG
    delta = node1.se + node2.se - new_se \
        + (node1.V*node1.log_V - node1.sum_b_log_b + node2.V*node2.log_V - node2.sum_b_log_b)/vG
    '''
    new_se = (new_V-new_s)/vG*log2(vG/new_V) + new_V*log2(new_V)/vG
    delta = node1.se + node2.se - new_se \
        + (node1.V*node1.log_V + node2.V*node2.log_V)/vG
    return delta


def get_delta_se(M, vG, parent, node1, node2):
    new_vs = node1.vs + node2.vs
    new_node_g = get_g(M, new_vs)
    new_node_V = get_v(M, new_vs)
    new_node_se = get_se(vG, new_node_g, new_node_V, parent.V)
    new_node1_se = get_se(vG, node1.g, node1.V, new_node_V)
    new_node2_se = get_se(vG, node2.g, node2.V, new_node_V)
    return node1.se + node2.se - new_node_se - new_node1_se - new_node2_se
