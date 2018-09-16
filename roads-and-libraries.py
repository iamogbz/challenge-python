#!/bin/python3
# https://www.hackerrank.com/contests/world-codesprint-8/challenges/torque-and-development


class Graph:
    size = None
    nodes = None

    def __init__(self, size):
        self.size = size
        self.nodes = [[] for i in range(size)]

    def connect(self, u, v):
        self.nodes[u] += [v]
        self.nodes[v] += [u]

    def get_components(self):
        seen = set()
        result = list()
        for i in range(self.size):
            if i not in seen:
                c = self.dfs(i)
                seen |= c
                result.append(len(c))

        return result

    def dfs(self, root):
        """
        Depth-first search
        """
        seen = set()
        stack = [root]
        while stack:  # not empty
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(self.nodes[n])

        return seen


q = int(input().strip())
for i in range(q):
    n, m, l, k = map(int, input().split())  # cities, roads, library, repair
    graph = Graph(n)
    for j in range(m):
        u, v = map(int, input().split())
        graph.connect(u - 1, v - 1)

    cost = 0
    if k >= l:
        cost = n * l
    else:
        cs = graph.get_components()
        s = len(cs)
        cost = (sum(cs) - s) * k + s * l
    print(cost)
