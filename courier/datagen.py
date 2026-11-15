"""Sample-data creation and loading (JSON)."""
import json
import random
from .models import Parcel
from .graph import Graph, random_graph


def random_parcels(n, num_nodes, seed=0):
    rng = random.Random(seed)
    return [Parcel(i + 1, rng.randrange(1, num_nodes), rng.randint(1, 15),
                   rng.randint(1, 5), rng.randint(1, 24)) for i in range(n)]


def save_dataset(path, parcels, graph, capacity):
    edges = sorted({(min(u, v), max(u, v), w) for u in graph.adj for v, w in graph.adj[u]})
    data = {"capacity": capacity, "nodes": graph.n, "edges": edges,
            "parcels": [vars(p) for p in parcels]}
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def load_dataset(path):
    with open(path) as f:
        d = json.load(f)
    g = Graph(d["nodes"])
    for u, v, w in d["edges"]:
        g.add_edge(u, v, w)
    return [Parcel(**p) for p in d["parcels"]], g, d["capacity"]


def make_dataset(num_parcels, num_nodes, capacity, seed):
    g = random_graph(num_nodes, extra_edges=num_nodes, seed=seed)
    return random_parcels(num_parcels, num_nodes, seed), g, capacity
