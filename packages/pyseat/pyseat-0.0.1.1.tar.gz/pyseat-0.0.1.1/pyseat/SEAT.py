import numpy as np
from math import log2
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering
import itertools

from . import se


class Node():
    def __init__(self, graph_stats, node_id, parent=None, leaf=False):
        self.id = node_id
        self.parent = parent
        self.leaf = leaf
        self.children = []
        self.left = 0
        self.right = 0
        self.g = 0.
        self.g_log_V = 0.
        self.V = 0.
        self.log_V = 0.
        self.V_log_V = 0.
        self.s = 0.
        self.se = 0.
        self.vs = []
        self.sum_b_log_b = 0.
        self.height = 0
        self.dist = 1
        self.graph_stats = graph_stats

    def __repr__(self):
        return self.toString()
        # return "Node()"

    def __str__(self):
        return self.toString()

    def toString(self):
        return "(idx:%d, %sdist:%d, [%d, %d], len(children)=%d, len(vs):%d)" % (self.id,
                                                                                'leaf, ' if self.leaf else '',
                                                                                self.dist, self.left, self.right,
                                                                                len(self.children),
                                                                                len(self.vs))

    def get_max_height(self):
        max_h = 0
        if not self.leaf:
            for child in self.children:
                if isinstance(child, Node):
                    h_tmp = child.get_max_height()
                    max_h = max(max_h, h_tmp)
        else:
            return self.height
        return max_h

    def reset(self, parent=None):
        self.init(parent)

    def init(self, parent=None):
        self.setBins()
        self.setV()
        self.setS()
        self.setG()
        if parent:
            self.setSE(parent)
        else:
            # root
            self.se = 0
        for c in self.children:
            if (isinstance(c, Node)):
                c.setSE(self)
        if self.leaf:
            self.children.sort()

    def setBins(self):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        vs = []
        if self.leaf:
            vs += self.children
            self.sum_b_log_b = np.sum(d_log_d[self.vs])
        else:
            for c in self.children:
                if isinstance(c, Node):
                    vs += c.setBins()
                elif isinstance(c, int):
                    vs.append(c)
                else:
                    raise TypeError('child can only be int or Node')
        self.vs = vs
        self.vs.sort()
        self.left = self.vs[0]
        self.right = self.vs[-1]
        return vs

    def setS(self):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        self.s = se.get_s(M, self.vs)

    def setG(self):
        self.g = self.V - self.s
        self.g_log_V = self.g * self.log_V
        # self.g = getG(self.vs)

    def setV(self):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        self.V = se.get_v(M, self.vs)
        self.log_V = log2(self.V)
        self.V_log_V = self.V * self.log_V

    def setSE(self, parent):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        self.se = se.get_se(vG, self.g, self.V, parent.V)

    def increase_height(self, increment=1):
        self.height += increment
        for c in self.children:
            if isinstance(c, Node):
                c.increase_height(increment)

    def merge(self, node_id, node1, node2, is_leaf=False):
        if (node1.parent != node2.parent):
            print("self=", self, "\nnode1=", node1, "\nnode2=", node2)
            raise ValueError("parents are not the same")
        node = Node(self.graph_stats, node_id, parent=self.id)
        node.leaf = is_leaf
        node.height = node1.height
        node1.parent = node.id
        node1.increase_height(1)
        node2.parent = node.id
        node2.increase_height(1)
        if is_leaf:
            node.children = node1.children + node2.children
        else:
            node.addChild(node1)
            node.addChild(node2)
        # print("before se=", node.se)
        node.reset(self)
        # print("after se=", node.se)
        self.addChild(node)
        if not self.delChild(node1):
            raise("fail to delete child", node1)
        if not self.delChild(node2):
            raise("fail to delete child", node1)
        # print("combine:\nself=", self, "\nnew node=", node, "\nnode1=", node1, "\nnode2=", node2)
        # print("node1.height=%d, node2.height=%d" % (node1.height, node2.height))
        return node

    def addChild(self, node):
        self.children.append(node)

    def delChild(self, node):
        idx = -1
        for i, c in enumerate(self.children):
            if c.id == node.id:
                idx = i
                break
        if idx >= 0:
            del self.children[idx]
            return True
        return False

    def printChildren(self):
        if all(isinstance(c, int) for c in self.children):
            print("\t".join(self.children))
        else:
            print("\t".join([c.id for c in self.children]))

    def verbose(self, k):
        print('-'*(k+1) + str(self))
        if len(self.children) > 0:
            for c in self.children:
                if isinstance(c, Node):
                    c.verbose(k+2)
                elif isinstance(c, int):
                    print("*"*(k+1+2) + str(c))
                else:
                    raise TypeError('child cannot be int or Node')

    def getNodes(self):
        nodes = []
        if not self.leaf:
            for c in self.children:
                nodes.append(c.vs)
                if isinstance(c, Node):
                    nodes.extend(c.getNodes())
                elif isinstance(c, int):
                    nodes.extend([c])
                else:
                    raise TypeError('child can only be int or Node')
        return nodes

    def getTreeSE(self):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        se = self.se
        # print(self, "g=", self.g, "v=", self.V, "se=", self.se, "vG=", vG)
        if self.leaf:
            se += (self.V_log_V - np.sum(d_log_d[self.children]))/vG
        else:
            for c in self.children:
                if isinstance(c, Node):
                    se += c.getTreeSE()
                elif isinstance(c, int):
                    print("getSEforBin(c, self.V)=", se.get_se_for_vertex(M, d, vG, c, self.V))
                    # se += getSEforBin(c, self.V)
                    se += (d[c]*self.log_V - d_log_d[c])/vG
                else:
                    raise TypeError('child can only be int or Node')
        return se


class SETree():

    def __init__(self, X, min_k=2, max_k=10,
                 strategy='merge_combine'):
        self.strategy = strategy
        self.min_k = min_k
        self.max_k = max_k
        self.ks = range(min_k, max_k+1)

        self.node_num = X.shape[0]
        self.node_id = -2
        self.node_list = {}

        self.graph_stats = self.graph_stats_init(X)

    def graph_stats_init(self, adj_m):
        M = adj_m
        # np.fill_diagonal(M, 0)
        d = np.sum(M, 1) - M.diagonal()
        if np.any(d == 0):
            M += 1e-3
            # np.fill_diagonal(M, 0)
            d = np.sum(M, 1) - M.diagonal()
        # print("d=", d)
        log_d = np.log2(d)
        d_log_d = np.multiply(d, log_d)
        # print("sum(d)=", sum(d))
        m = np.sum(np.triu(M, 1))
        # print("m=", m)
        vG = np.sum(M)
        # print("vG=", vG)
        log_vG = log2(vG)

        graph_stats = M, m, d, log_d, d_log_d, vG, log_vG
        return graph_stats

    def get_node_id(self):
        self.node_id += 1
        return self.node_id

    def build_tree(self, X):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        root = Node(self.graph_stats, self.get_node_id())
        self.node_list[root.id] = root
        root.V = 2.*m  # ???
        for i in range(self.node_num):
            node = Node(self.graph_stats, self.get_node_id(), parent=root.id, leaf=True)
            self.node_list[node.id] = node
            node.height = 1
            node.children = [i]
            node.left = node.right = i
            node.init(root)
            root.addChild(node)
        root.reset()
        # root.verbose(0)
        Z = self.linkage(root)
        # print(Z)
        return Z

    def linkage(self, root, by='table'):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        n = self.node_num
        Z = np.zeros((n - 1, 5))
        delta_m = np.zeros((2*n - 1, 2*n - 1))
        delta_m.fill(-10000)
        leafs = list(range(n))
        singletons = list(range(n))

        # merge with delta_se_plus to eliminate any singletons
        for n1, n2 in itertools.combinations(range(n), 2):
            node1 = self.node_list[n1]
            node2 = self.node_list[n2]
            delta_m[n1, n2] = se.get_delta_se_plus(M, vG, d, root, node1, node2)

        z_i = 0
        while singletons:
            tmp = delta_m[np.ix_(singletons, leafs)]
            max_i = np.argmax(tmp)
            row_i = int(max_i/tmp.shape[1])
            col_i = max_i % tmp.shape[1]
            max_delta = tmp[row_i, col_i]
            max_n1 = self.node_list[singletons[row_i]]
            max_n2 = self.node_list[leafs[col_i]]

            new_node = root.merge(self.get_node_id(), max_n1, max_n2, is_leaf=True)
            self.node_list[new_node.id] = new_node

            Z[z_i] = [max_n1.id, max_n2.id, new_node.dist, len(max_n1.vs) + len(max_n2.vs), max_delta]

            # update
            singletons.remove(max_n1.id)
            if max_n2.id in singletons:
                singletons.remove(max_n2.id)
            if max_n1.id in leafs:
                leafs.remove(max_n1.id)
            leafs.remove(max_n2.id)
            leafs.append(new_node.id)
            for s_i in singletons:
                node = self.node_list[s_i]
                delta_m[s_i, new_node.id] = se.get_delta_se_plus(M, vG, d, root, node, new_node)

            z_i += 1

        self.leafs = [l for l in leafs]
        # merge the node clusters with delta_se

        for n1, n2 in itertools.combinations(leafs, 2):
            node1 = self.node_list[n1]
            node2 = self.node_list[n2]
            delta_m[n1, n2] = se.get_delta_se(M, vG, root, node1, node2)
            # delta_m[n1, n2] = se.get_delta_se_plus(M, vG, d, root, node1, node2)

        while z_i < n - 1:
            tmp = delta_m[np.ix_(leafs, leafs)]
            max_i = np.argmax(tmp)
            row_i = int(max_i/tmp.shape[1])
            col_i = max_i % tmp.shape[1]
            max_delta = tmp[row_i, col_i]
            max_n1 = self.node_list[leafs[row_i]]
            max_n2 = self.node_list[leafs[col_i]]

            new_node = root.merge(self.get_node_id(), max_n1, max_n2, is_leaf=False)
            self.node_list[new_node.id] = new_node
            new_node.dist = max(max_n1.dist, max_n2.dist) + 1

            Z[z_i] = [max_n1.id, max_n2.id, new_node.dist, len(max_n1.vs) + len(max_n2.vs), max_delta]

            # update
            leafs.remove(max_n1.id)
            leafs.remove(max_n2.id)
            for l_i in leafs:
                node = self.node_list[l_i]
                delta_m[l_i, new_node.id] = se.get_delta_se(M, vG, root, node, new_node)
                # delta_m[l_i, new_node.id] = se.get_delta_se_plus(M, vG, d, root, node, new_node)
            leafs.append(new_node.id)

            z_i += 1

        Z[:, 4] = -Z[:, 4] + abs(min(-Z[:, 4])) + 0.1
        # Z[:, 2] = Z[:, 4]
        return Z

    # ineffient version, for stratedy testing
    def linkage_back(self, root):
        n = self.node_num
        Z = np.zeros((n - 1, 4))
        for i in range(n - 1):
            root, max_n1, max_n2, max_delta = self.linkage_merge(root)
            if max_n1 is None and max_n2 is None:
                # root, max_n1, max_n2, max_delta = self.linkage_combine(root)
                root, max_n1, max_n2, max_delta = self.linkage_merge(root)
            d = max(max_n1.dist, max_n2.dist) + 1
            Z[i] = [max_n1.id, max_n2.id, d, len(max_n1.vs) + len(max_n2.vs)]
            # Z[:, 2] = -Z[:, 2] + abs(min(-Z[:, 2])) + 0.00001
            # Z[:, 2] = 1/Z[:, 2]
        return Z

    def linkage_merge(self, root):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats

        max_delta, max_n1, max_n2 = -100000, None, None
        max_n1, max_n2 = None, None
        for node1, node2 in itertools.combinations(root.children, 2):
            if len(node1.children) > 1 and len(node2.children) > 1:
                continue
            delta = se.get_delta_se_plus(M, vG, d, root, node1, node2)
            if delta > max_delta:
                max_delta, max_n1, max_n2 = delta, node1, node2

        if max_n1 is not None and max_n2 is not None:
            root.merge(self.get_node_id(), max_n1, max_n2, is_leaf=True)
        return root, max_n1, max_n2, max_delta

    def linkage_combine(self, root):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats

        max_delta, max_n1, max_n2 = -100000, None, None
        max_n1, max_n2 = None, None
        for node1, node2 in itertools.combinations(root.children, 2):
            delta = se.get_delta_se(M, vG, root, node1, node2)
            if delta > max_delta:
                max_delta, max_n1, max_n2 = delta, node1, node2

        new_node = root.merge(self.get_node_id(), max_n1, max_n2)
        self.node_list[new_node.id] = new_node
        new_node.dist += max(max_n1.dist, max_n2.dist) + 1
        return root, max_n1, max_n2, max_delta

    def linkage_aux(self, root):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats

        max_delta, max_n1, max_n2 = -100000, None, None
        max_n1, max_n2 = None, None
        for node1, node2 in itertools.combinations(root.children, 2):
            if len(node1.children) > 1 or len(node2.children) > 1:
                delta = se.get_delta_se_plus(M, vG, d, root, node1, node2)
            else:
                delta = se.get_delta_se(M, vG, root, node1, node2)
            if delta > max_delta:
                max_delta, max_n1, max_n2 = delta, node1, node2
        if len(max_n1.children) < 1 or len(max_n2.children) < 1:
            root.merge(self.get_node_id(), max_n1, max_n2, is_leaf=True)
        else:
            new_node = root.merge(self.get_node_id(), max_n1, max_n2)
            self.node_list[new_node.id] = new_node
            new_node.dist += max(max_n1.dist, max_n2.dist) + 1
        return root, max_n1, max_n2, max_delta

    def linkage_aux_simple(self, root):

        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats

        max_delta, max_n1, max_n2 = -100000, None, None
        max_n1, max_n2 = None, None
        for node1, node2 in itertools.combinations(root.children, 2):
            delta = se.get_delta_se_plus(M, vG, root, node1, node2)
            if delta > max_delta:
                max_delta, max_n1, max_n2 = delta, node1, node2
        new_node = root.merge(self.get_node_id(), max_n1, max_n2)
        self.node_list[new_node.id] = new_node
        new_node.dist += max(max_n1.dist, max_n2.dist) + 1
        return root, max_n1, max_n2, max_delta

    def cut_tree(self, Z, n_clusters):
        # update node distance
        root = self.node_list[self.node_id]
        self._update_dist_to_level(root, Z)
        se_scores, clusters = self._cut_tree_dp(root)
        self.se_scores = se_scores[1:]

        clusters = np.matrix(clusters).T
        self.Z_clusters = hierarchy.cut_tree(Z[:, :4], n_clusters=n_clusters)
        return clusters

    def _cut_tree_dp(self, root):
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        nodes = [node_id for node_id, node in self.node_list.items() if not node.leaf and node.id != -1]
        # print(nodes)  # the nodes ordered from child to parent
        max_k = len(self.leafs)
        if max_k < self.max_k:
            self.max_k = max_k
            self.ks = range(2, max_k + 1)
        # print('max_k', max_k)
        cost_m = np.zeros((self.max_k, len(nodes)))
        cost_m.fill(100)
        cutoff_m = np.zeros((self.max_k, len(nodes)))
        cutoff_m.fill(-1)
        np.set_printoptions(suppress=True)

        for k in self.ks:
            self._cut_tree_dp_recursive(root, root, k, vG, cost_m, cutoff_m, nodes)
        # print(cost_m)
        # print(cutoff_m)
        clusters = []
        self._trace_back(root, cost_m, cutoff_m, nodes, clusters)

        clusters = [(v, i) for i, c in enumerate(clusters) for v in self.node_list[c].vs]
        clusters = sorted(clusters)
        clusters = [c for v, c in clusters]
        return cost_m[:, -1], clusters

    def _trace_back(self, node, cost_m, cutoff_m, nodes, clusters):
        if node.leaf:
            return

        i = nodes.index(node.id)
        k_hat = cost_m.shape[0]-np.argmin(cost_m[:, i][::-1])
        k_prime = int(cutoff_m[k_hat-1, i])
        # print(node.id, k_hat, k_prime)
        left_node, right_node = node.children

        if k_prime > 1:
            self._trace_back(left_node, cost_m, cutoff_m, nodes, clusters)
        else:
            clusters.append(left_node.id)
        if k_prime < k_hat-1:
            self._trace_back(right_node, cost_m, cutoff_m, nodes, clusters)
        else:
            clusters.append(right_node.id)

    def _cut_tree_dp_recursive(self, parent, node, k, vG, cost_m, cutoff_m, nodes):
        if k == 1:
            # print(se.get_se(vG, node.g, node.V, parent.V) == node.se)
            cost = node.g/vG*log2(vG/node.V) - node.g/vG*log2(parent.V/node.V) + node.se
            if not node.leaf:
                cost_m[k-1, nodes.index(node.id)]
            return cost
        if node.leaf:
            return 10000

        min_cost = 100000000
        min_i = None
        for i in range(1, k):
            cost = self._cut_tree_dp_recursive(node, node.children[0], i, vG, cost_m, cutoff_m, nodes) + \
                self._cut_tree_dp_recursive(node, node.children[1], k-i, vG, cost_m, cutoff_m, nodes)
            if cost < min_cost:
                min_cost = cost
                min_i = i
        # print('k', k, 'min_cost', min_cost, node, node.children[0].id, node.children[1].id, min_i, k)
        cost_m[k-1, nodes.index(node.id)] = min_cost
        cutoff_m[k-1, nodes.index(node.id)] = min_i
        return min_cost

    def _update_dist_to_level(self, parent, Z):
        for c in parent.children:
            c.reset(parent)
            if c.leaf:
                c.reset(parent)
                continue
            c.dist = parent.dist - 1
            if c.id > self.node_num:
                Z[c.id-self.node_num, 2] = c.dist
            self._update_dist_to_level(c, Z)

    def _cut_tree_not_good(self, clusters, Z, dist, k):  # binary tree
        # print('dist', dist)
        M, m, d, log_d, d_log_d, vG, log_vG = self.graph_stats
        if len(clusters) >= k:
            for c in clusters:
                c.dist = dist
                if c.id > self.node_num:
                    Z[c.id-self.node_num, 2] = dist
                    pass
            # print('k', k, clusters)
            return clusters
        max_delta_se = -10000
        max_c = None
        for c in clusters:
            if c.leaf:
                continue
            delta_se = se.get_delta_se(M, vG, c, c.children[0], c.children[1])
            if delta_se > max_delta_se:
                max_delta_se = delta_se
                max_c = c
        # update clusters, dist, and Z
        max_c.dist = dist
        if max_c.id > self.node_num:
            Z[max_c.id-self.node_num, 2] = dist
            pass
        clusters.remove(max_c)
        clusters += max_c.children
        # print('c', k, clusters)
        return self._cut_tree(clusters, Z, dist-1, k)


class SEClustering(AgglomerativeClustering):

    def __init__(self, n_clusters=2,
                 affinity='precomputed',
                 strategy='merge_combine'
                 ):
        super().__init__(self)
        self.n_clusters = n_clusters
        self.affinity = affinity
        self.strategy = strategy

    def fit(self, X, y=None):
        """Fit the structural entropy clustering from features, or distance matrix.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features) or (n_samples, n_samples)
            Training instances to cluster, or distances between instances if
            ``affinity='precomputed'``.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self
        """

        X = self._validate_data(X, ensure_min_samples=2, estimator=self)

        '''
        if self.n_clusters is not None and self.n_clusters <= 0:
            raise ValueError("n_clusters should be an integer greater than 0."
                             " %s was provided." % str(self.n_clusters))
        '''

        if self.affinity not in ['precomputed', 'euclidean']:
            raise ValueError("affinity should be precomputed, euclidean."
                             " %s was provided." % str(self.affinity))

        if self.strategy not in ['merge_combine', 'agg']:
            raise ValueError("affinity should be merge_combine, agg."
                             " %s was provided." % str(self.strategy))

        # build the tree
        se_tree = SETree(X, strategy=self.strategy)
        Z = se_tree.build_tree(X)
        se_tree.cut_tree(Z[:, :4], self.n_clusters)
        if type(self.n_clusters) == int:
            self.labels_ = se_tree.Z_clusters.T[0]
        else:
            self.labels_ = se_tree.Z_clusters.T
        self.Z_ = Z[:, :4]

        return self


class SEAT(SEClustering):

    def __init__(self, min_k=2, max_k=10,
                 affinity='precomputed',
                 strategy='merge_combine'
                 ):
        self.min_k = min_k
        self.max_k = max_k
        self.ks = range(min_k, max_k+1)
        self.affinity = affinity
        self.strategy = strategy

    def fit(self, X, y=None):

        X = self._validate_data(X, ensure_min_samples=2, estimator=self)

        if self.min_k is not None and self.min_k <= 1:
            raise ValueError("min_k should be an integer greater than 1."
                             " %s was provided." % str(self.min_k))

        if self.max_k is not None and self.max_k <= 2:
            raise ValueError("max_k should be an integer greater than 2."
                             " %s was provided." % str(self.max_k))

        if self.affinity not in ['precomputed', 'euclidean']:
            raise ValueError("affinity should be precomputed, euclidean."
                             " %s was provided." % str(self.affinity))

        if self.strategy not in ['merge_combine', 'agg']:
            raise ValueError("affinity should be merge_combine, agg."
                             " %s was provided." % str(self.strategy))

        # build the tree
        se_tree = SETree(X, self.min_k, self.max_k, strategy=self.strategy)
        Z = se_tree.build_tree(X)
        clusters = se_tree.cut_tree(Z, self.ks).T.tolist()[0]
        '''
        labels = {}
        for i in range(clusters.shape[0]):
            cs = clusters[i].tolist()[0]
            labels[len(set(cs))] = cs
        '''
        self.ks = list(se_tree.ks)
        self.se_scores = se_tree.se_scores
        self.labels_ = clusters
        self.optimal_k = len(set(clusters))
        self.Z_ = Z[:, :4]

        return self
