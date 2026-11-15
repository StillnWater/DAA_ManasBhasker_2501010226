"""Phase 3a: road network (undirected weighted graph, adjacency list) and Dijkstra."""
import heapq
import random


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = {i: [] for i in range(n)}

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def edge_count(self):
        return sum(len(v) for v in self.adj.values()) // 2


def dijkstra(graph, src):
    """Shortest distance from src to every node, plus predecessors to rebuild paths.
    Binary-heap version: O((V + E) log V). Edge weights must be non-negative."""
    dist = {v: float("inf") for v in graph.adj}
    prev = {v: None for v in graph.adj}
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                      # stale heap entry
        for v, w in graph.adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def build_path(prev, src, dst):
    path = []
    while dst is not None:
        path.append(dst)
        dst = prev[dst]
    path.reverse()
    return path if path and path[0] == src else []


def random_graph(n, extra_edges, seed=0, max_w=20):
    """Connected random graph: a random spanning tree plus extra edges. Node 0 is the depot."""
    rng = random.Random(seed)
    g = Graph(n)
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):
        g.add_edge(nodes[i], nodes[rng.randrange(i)], rng.randint(1, max_w))
    existing = {(min(u, v), max(u, v)) for u in g.adj for v, _ in g.adj[u]}
    attempts = 0
    while extra_edges > 0 and attempts < extra_edges * 20:
        attempts += 1
        u, v = rng.sample(range(n), 2)
        key = (min(u, v), max(u, v))
        if key not in existing:
            existing.add(key)
            g.add_edge(u, v, rng.randint(1, max_w))
            extra_edges -= 1
    return g
