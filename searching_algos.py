"""https://en.wikipedia.org/wiki/Search_algorithm"""


from math import inf


def binary(graph: "Graph", target, source=None):
    """
    Binary tree search
    https://en.wikipedia.org/wiki/Binary_search_algorithm
    """
    return target


def _fs(graph: "Graph", value, root=None, pos=0):
    """
    Abstract search algo to highlight traversal diff between breadth and depth first
    :param pos: 0 for queue, -1 for stack, defaults to 0
    """
    visited_nodes = set()
    search_nodes = [root]
    # next_nodes = set(search_nodes)
    while search_nodes:
        curr_node = search_nodes.pop(pos)  # use FIFO for BFS and LIFO for DFS
        # print(search_nodes, curr_node, visited_nodes, graph.get_adjacent(curr_node))
        if curr_node in visited_nodes:
            continue
        elif curr_node is not None:
            visited_nodes.add(curr_node)

        for next_node in graph.get_adjacent(curr_node):
            if curr_node is not None:
                conn_value = graph.get_value(curr_node, next_node)
                if conn_value == value:
                    return (curr_node, next_node)
            if next_node not in visited_nodes and next_node not in search_nodes:
                # next_nodes.add(next_node)
                search_nodes.append(next_node)

    return (None, None)


def bfs(graph: "Graph", value, root=None):
    """
    Breadth first search
    https://en.wikipedia.org/wiki/Breadth-first_search
    """
    return _fs(graph, value, root, 0)


def dfs(graph: "Graph", value, root=None):
    """
    Depth first search
    https://en.wikipedia.org/wiki/Depth-first_search
    """
    return _fs(graph, value, root, -1)


def dijkstra(graph: "Graph", target, source=None):
    """
    Dijkstra
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    NOTE: see BFS
    """
    # print("target", target)
    dist = {source: 0}
    visited_nodes = set()
    # queue = {source, *graph.get_adjacent(source)}
    # initialise the queue with the source or all nodes if no source given
    queue = [source] if source else graph.get_adjacent(source)

    while queue:
        q = list(
            (n, dist.get(n, inf), i)
            for i, n in enumerate(queue)
            if n is not None and n not in visited_nodes
        )
        (min_v, min_dist_v, min_idx) = min(q)
        # print("min", min_v, min_dist_v, graph.get_adjacent(min_v))
        # target currently has the lowest distance amongst remaining possible steps
        if target == min_v:
            break

        visited_nodes.add(queue.pop(min_idx))

        for nxt_v in graph.get_adjacent(min_v):
            # print("dist", dist, nxt_v, visited_nodes)
            if nxt_v in visited_nodes:
                continue
            conn_w = graph.get_value(min_v, nxt_v)
            nxt_dist_v = (min_dist_v if min_v in dist else 0) + conn_w
            if nxt_v not in dist or nxt_dist_v < dist[nxt_v]:
                dist[nxt_v] = nxt_dist_v
            queue.append(nxt_v)

    # print(dist)
    return dist.get(target, inf)


class Graph:
    """Graph tree data structure"""

    _bidi = True  # defaults to true for undirected graphs
    _data = {}

    def __repr__(self):
        return repr((">" + ("<" if self.is_bidirectional else ">"), self._data))

    def set_bidirectionality(self, enabled: "bool"):
        """Toggle if the graph operations should be bidirectional"""
        self._bidi = enabled

    @property
    def data(self):
        """Data getter"""
        return self._data

    @property
    def is_bidirectional(self):
        """Getter for graph bidirectionality"""
        return self._bidi

    def insert(self, source, target, value, reverse=None):
        """Insert source vertex and directed edge to target with weight value"""
        if not self._data.get(source, None):
            self._data[source] = {}
        self._data[source][target] = value

        if reverse is not None:  # or self.is_bidirectional:
            if not self._data.get(target, None):
                self._data[target] = {}
            self._data[target][source] = value if reverse is None else reverse

    def remove(self, source, target):
        """Remove vertex edge from map including the reverse direction if bidirectional"""

        def _remove(s, t):
            if s not in self._data or t not in self._data[s]:
                return
            del self._data[s][t]
            if not self._data[s]:
                del self._data[s]

        _remove(source, target)
        if self.is_bidirectional:
            _remove(target, source)

    def retarget(self, old_target, new_target):
        """Replace all edges to previous source with new target"""
        for src, src_targets in self._data.items():
            if old_target in src_targets:
                self.insert(src, new_target, src_targets[old_target])
                self.remove(src, old_target)

        if self._data.get(old_target, None):
            self._data[new_target] = self._data[old_target]
            del self._data[old_target]

    def get_adjacent(self, node=None):
        """Get all nodes/vertexes directly connected to this one or all when node is None"""
        forward_conns = self._data.get(node, self._data if node is None else {}).keys()

        reverse_conns = set()
        if self.is_bidirectional or node is None:
            for src, src_targets in self._data.items():
                if node in src_targets:  # always false when None
                    reverse_conns.add(src)
                elif node is None:
                    reverse_conns.update(src_targets.keys())

        return [*reverse_conns.union(forward_conns)]

    def get_value(self, source, target):
        """Get weight value for source target edge connection"""
        branch_leaves = set(self._data.get(source, {}).keys())
        if not target in branch_leaves:
            if source in self._data.get(target, {}) and self.is_bidirectional:
                return self._data[target][source]
            return None
            # raise KeyError(
            #     f"[{target}] target does not exist at source [{source}]: {branch_leaves}"
            # )
        return self._data[source][target]


g = Graph()
g.insert(0, 1, 1)
g.insert(0, 2, 1)
g.insert(1, 3, 1)
g.insert(1, 4, 1)
g.insert(3, 5, 1)
g.insert(3, 6, 1)
# g.set_bidirectionality(False)
print("g", g)
print(bfs(g, 6, 0))
print(dfs(g, 6, 0))
# print("0", g.get_adjacent(0))
# print("1", g.get_adjacent(1))
# g.retarget(1, 3)
# print("g", g)
# print("[0:3]", g.get_value(0, 3))
# print("[3:0]", g.get_value(3, 0))
# g.set_bidirectionality(False)
# g.remove(1, 3)
# print("g", g)
# print("*", g.get_adjacent())
# print("[0:3]", g.get_value(0, 3))
# print("[3:0]", g.get_value(3, 0))
print(dijkstra(g, 6))