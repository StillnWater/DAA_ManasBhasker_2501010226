"""Integrates all phases: sort -> knapsack -> Dijkstra -> nearest-neighbour route."""
import time
from .sorting import merge_sort, parcel_key
from .knapsack import knapsack
from .graph import dijkstra, build_path
from .tsp import nearest_neighbor

DEPOT = 0


def plan(parcels, graph, capacity):
    t = {}
    s = time.perf_counter()
    ordered = merge_sort(parcels, key=parcel_key)
    t["sort"] = time.perf_counter() - s

    s = time.perf_counter()
    best_value, chosen, dp = knapsack(ordered, capacity)
    t["knapsack"] = time.perf_counter() - s

    stops = sorted({p.dest for p in chosen if p.dest != DEPOT})
    s = time.perf_counter()
    sources = [DEPOT] + stops
    dist, prev = {}, {}
    for u in sources:                       # one Dijkstra run per stop (+ depot)
        d, p = dijkstra(graph, u)
        dist[u] = d
        prev[u] = p
    t["dijkstra"] = time.perf_counter() - s

    s = time.perf_counter()
    order, length = nearest_neighbor(dist, DEPOT, stops)
    t["tsp"] = time.perf_counter() - s

    # Expand the stop order into the actual road path (through intermediate junctions).
    full_path = [DEPOT]
    for a, b in zip(order, order[1:]):
        full_path += build_path(prev[a], a, b)[1:]

    return {
        "sorted": ordered, "chosen": chosen, "value": best_value, "dp": dp,
        "stops": stops, "order": order, "length": length, "dist": dist,
        "full_path": full_path, "times": t,
    }
