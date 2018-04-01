import time
    
# Graph: simple undirected OR symmetric loopless directed
class Graph:
    INF = None
    size = None
    nodes = None
    # edges = None # unneccessary for unweighted graph
    
    def __init__(self, size):
        self.size = size
        self.INF = size * size
        self.nodes = [[] for i in range(size)]
        # self.edges = [[-1]*size for i in range(size)]
    
    def connect(self, u, v, l=1):
        self.nodes[u] += [v]
        self.nodes[v] += [u]
        # self.edges[u][v] = l
        # self.edges[v][u] = l
    
    # dijkstra shortest path
    def path(self, s, t=None):
        d = [self.INF]*self.size                 # initialise all distances to infinity
        # p = [None]*self.size                   # set shortest previous path to none
        queue = set(range(self.size))            # queue all nodes
        
        d[s] = 0                                 # distance from s to s
        
        while queue:                             # not empty
            u = min(queue, key=lambda x: d[x])   # minimum distance node in queue
            queue.remove(u)                      # removal to mark as visited
            if t:                                # if there is a target
                if u == t: break                 # we've hit the target
                if d[u] == self.INF: return -1   # minimum distance is infinity 
            for v in set(self.nodes[u]) & queue: # neighbour nodes still in queue
                alt = d[u] + 1 # edges[u][v]     # path(s,v) = path(s,u) + path(u,v)
                if alt < d[v]:                   # if smaller then shorter path found
                    d[v] = alt                   # set path(s,v) to new length
                    # p[v] = u                   # set shortest previous path
        
        return d[t] if t else d #,p              # if no target return all distances
    

# num test cases
t = int(input())
for i in range(t):
    n,m = map(int,input().split())
    graph = Graph(n)
    a_time = time.time()
    for i in range(m):
        x,y = map(int,input().split())
        graph.connect(x-1,y-1) 
    b_time = time.time()
    print("filling:", round(b_time - a_time, 3), "secs")
    s = int(input())
    a_time = time.time()
    costs = graph.path(s-1)
    b_time = time.time()
    print(costs[0])
    print("mapping:", round(b_time - a_time, 3), "secs")
    
