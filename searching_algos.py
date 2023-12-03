"""https://en.wikipedia.org/wiki/Search_algorithm"""


from math import inf
from _algos import Graph


def binary(graph: "Graph", target):
    """
    Binary tree search
    https://en.wikipedia.org/wiki/Binary_search_algorithm
    """
    bst = graph.binarytree
    end = len(bst)
    start = 0
    while len(bst[start:end]) > 1:
        current = start + (end - start) // 2
        v = bst[current]
        if v == target:
            return target
        elif v > target:
            end = current
        else:
            start = current
    return None


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
            nxt_dist_v = (min_dist_v if min_v in dist else 0) + (conn_w or 0)
            if nxt_v not in dist or nxt_dist_v < dist[nxt_v]:
                dist[nxt_v] = nxt_dist_v
            queue.append(nxt_v)

    # print(dist)
    return dist.get(target, inf)


def test_graph():
    g = Graph()
    g.insert(0, 1, 1)
    g.insert(0, 2, 1)
    g.insert(1, 3, 1)
    g.insert(1, 4, 1)
    g.insert(3, 5, 1)
    g.insert(3, 6, 1)
    # g.set_bidirectionality(False)
    # print("g", g)
    # print(bfs(g, 6, 0))
    # print(dfs(g, 6, 0))
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
    return g


def test_graph_methods():
    """test graph creation and modification"""
    print(test_graph())
    print(test_graph().as_binarytree())


def test_dijkstra_pathing():
    """test path finding in a graph using dijkstra"""
    print(dijkstra(test_graph(), 6))


def test_binary_search_tree():
    """test binary search tree"""
    print(binary(test_graph(), (3, 6, 1)))
    print(binary(test_graph(), (3, 6, 2)))


test_graph_methods()
test_dijkstra_pathing()
test_binary_search_tree()
