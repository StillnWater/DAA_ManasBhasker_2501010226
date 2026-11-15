"""Phase 3b: delivery order with the nearest-neighbour TSP heuristic.

Greedy: from the current stop always drive to the closest unvisited stop, then return to depot.
Time O(k^2) for k stops (distances come from Dijkstra). It is an approximation, not optimal.
"""
from itertools import permutations


def nearest_neighbor(dist, depot, stops):
    """dist[a][b] = shortest-path distance. Returns (order, total_length) as a closed tour."""
    remaining, order, cur, total = set(stops), [depot], depot, 0
    while remaining:
        nxt = min(remaining, key=lambda s: (dist[cur][s], s))   # tie-break on node id
        total += dist[cur][nxt]
        order.append(nxt)
        remaining.remove(nxt)
        cur = nxt
    total += dist[cur][depot]
    order.append(depot)
    return order, total


def brute_force_tour(dist, depot, stops):
    """Exact optimum by trying every ordering, O(k!). Only for tiny k, to judge the heuristic."""
    best, best_len = None, float("inf")
    for perm in permutations(stops):
        route = [depot, *perm, depot]
        length = sum(dist[a][b] for a, b in zip(route, route[1:]))
        if length < best_len:
            best, best_len = route, length
    return best, best_len
