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
        while stack: # not empty
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(self.nodes[n])
            
        return seen
    

n = int(input().strip())
m = int(input().strip())
graph = Graph(n*m)
a_time = time.time()
p = list(map(int, input().split()))
# build graph
for i in range(n-1):
    not_last_row = i+1 < n
    if not_last_row: q = list(map(int, input().split()))
    
    for j in range(m):
        not_last_col = j+1 < m
        if p[j]: # if value is 1
            node = i*m+j
            if not_last_col:
                if p[j+1]: graph.connect(node, node+1)
                if not_last_row and q[j+1]: graph.connect(node, node+1+m)
            if not_last_row:
                if q[j]: graph.connect(node, node+m)
                if j > 0 and q[j-1]: graph.connect(node, node-1+m)
        
    p = q

b_time = time.time()
print("filling:", round(b_time - a_time, 3), "secs")
a_time = time.time()
c = graph.get_components()
b_time = time.time()
print("mapping:", round(b_time - a_time, 3), "secs")
a_time = time.time()
print(max(c))
print("get max:", round(b_time - a_time, 3), "secs")
b_time = time.time()
