"""Correctness checks. Run: python tests.py"""
import random
from itertools import combinations
from courier.sorting import merge_sort, insertion_sort, quick_sort, parcel_key
from courier.knapsack import knapsack
from courier.graph import Graph, dijkstra, random_graph
from courier.tsp import nearest_neighbor, brute_force_tour
from courier.datagen import random_parcels
from courier.planner import plan


def test_sorting():
    ps = random_parcels(200, 20, seed=5)
    expected = sorted(ps, key=parcel_key)
    assert merge_sort(ps, parcel_key) == expected
    assert insertion_sort(ps, parcel_key) == expected
    assert quick_sort(ps, parcel_key) == expected
    assert merge_sort([]) == [] and merge_sort([3]) == [3]
    assert merge_sort([3, 1, 2, 1]) == [1, 1, 2, 3]


def test_knapsack_vs_bruteforce():
    for seed in range(20):
        ps = random_parcels(10, 10, seed)
        cap = 30
        val, chosen, _ = knapsack(ps, cap)
        best = max(sum(p.value for p in c)
                   for r in range(len(ps) + 1) for c in combinations(ps, r)
                   if sum(p.weight for p in c) <= cap)
        assert val == best, (seed, val, best)
        assert sum(p.weight for p in chosen) <= cap
        assert sum(p.value for p in chosen) == val
    assert knapsack([], 10)[0] == 0
    assert knapsack(random_parcels(5, 5, 0), 0)[0] == 0


def floyd(g):
    d = [[float("inf")] * g.n for _ in range(g.n)]
    for u in g.adj:
        d[u][u] = 0
        for v, w in g.adj[u]:
            d[u][v] = min(d[u][v], w)
    for k in range(g.n):
        for i in range(g.n):
            for j in range(g.n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def test_dijkstra_vs_floyd():
    for seed in range(10):
        g = random_graph(25, 30, seed)
        fw = floyd(g)
        for s in (0, 7, 24):
            dist, _ = dijkstra(g, s)
            assert all(dist[v] == fw[s][v] for v in range(g.n))
    g = Graph(3); g.add_edge(0, 1, 4)              # node 2 is unreachable
    assert dijkstra(g, 0)[0][2] == float("inf")


def test_tsp_heuristic():
    for seed in range(10):
        g = random_graph(15, 20, seed)
        stops = random.Random(seed).sample(range(1, 15), 6)
        dist = {u: dijkstra(g, u)[0] for u in [0] + stops}
        order, length = nearest_neighbor(dist, 0, stops)
        _, opt = brute_force_tour(dist, 0, stops)
        assert order[0] == order[-1] == 0 and sorted(order[1:-1]) == sorted(stops)
        assert length >= opt                         # heuristic can never beat the optimum


def test_end_to_end():
    ps = random_parcels(50, 30, seed=9)
    g = random_graph(30, 30, seed=9)
    r = plan(ps, g, 60)
    assert sum(p.weight for p in r["chosen"]) <= 60
    assert r["full_path"][0] == r["full_path"][-1] == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("All tests passed.")
