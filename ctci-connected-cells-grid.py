# https://www.hackerrank.com/challenges/ctci-connected-cell-in-a-grid

import time


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
        result = set()
        for i in range(self.size):
            if i not in seen:
                c = self.dfs(i)
                seen |= c
                result.add(len(c))

        return result

    # Depth-first search
    def dfs(self, root):
        seen = set()
        stack = [root]
        while stack:  # not empty
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(self.nodes[n])

        return seen


num_rows = int(input().strip())
num_cols = int(input().strip())
graph = Graph(num_rows * num_cols)
time_a = time.time()
curr_row = list(map(int, input().split()))
# build graph
for i in range(num_rows - 1):
    not_last_row = i + 1 < num_rows
    if not_last_row:
        next_row = list(map(int, input().split()))

    for j in range(num_cols):
        not_last_col = j + 1 < num_cols
        if curr_row[j]:  # if value is 1
            node = i * num_cols + j
            if not_last_col:
                if curr_row[j + 1]:
                    graph.connect(node, node + 1)
                if not_last_row and next_row[j + 1]:
                    graph.connect(node, node + 1 + num_cols)
            if not_last_row:
                if next_row[j]:
                    graph.connect(node, node + num_cols)
                if j > 0 and next_row[j - 1]:
                    graph.connect(node, node - 1 + num_cols)
    curr_row = next_row

time_b = time.time()
print("filling:", round(time_b - time_a, 3), "secs")
time_a = time.time()
comps = graph.get_components()
time_b = time.time()
print("mapping:", round(time_b - time_a, 3), "secs")
time_a = time.time()
print(max(comps))
print("get max:", round(time_b - time_a, 3), "secs")
time_b = time.time()
