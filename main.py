"""Mini-Courier Planner demo.   python main.py [dataset.json]"""
import sys
from courier.datagen import load_dataset
from courier.planner import plan
from courier.tsp import brute_force_tour


def show(path):
    parcels, graph, capacity = load_dataset(path)
    print(f"Dataset: {path}")
    print(f"Parcels: {len(parcels)} | Road graph: {graph.n} nodes, {graph.edge_count()} roads | "
          f"Van capacity: {capacity} kg\n")
    r = plan(parcels, graph, capacity)

    print("== Phase 2a: parcels sorted by urgency (deadline, then priority) ==")
    print(f"{'Parcel':>6} {'Dest':>5} {'Wt(kg)':>7} {'Prio':>5} {'Deadline(h)':>12} {'Value':>6}")
    for p in r["sorted"]:
        print(f"{p.id:>6} {p.dest:>5} {p.weight:>7} {p.priority:>5} {p.deadline:>12} {p.value:>6}")

    print(f"\n== Phase 2b: knapsack (DP) - best parcels for one trip, capacity {capacity} kg ==")
    n = len(parcels)
    if n <= 15:   # print a readable slice of the DP table (every 5 kg) for small datasets
        cols = list(range(0, capacity + 1, 5))
        print("DP table dp[i][w] (columns = capacity in kg):")
        print("  i  " + " ".join(f"{w:>4}" for w in cols))
        for i, row in enumerate(r["dp"]):
            print(f"{i:>3}  " + " ".join(f"{row[w]:>4}" for w in cols))
    tw = sum(p.weight for p in r["chosen"])
    print(f"Selected parcels: {[p.id for p in r['chosen']]}")
    print(f"Total weight: {tw}/{capacity} kg | Total value: {r['value']}")
    left = [p.id for p in r["sorted"] if p not in r["chosen"]]
    print(f"Left for next trip: {left}")

    print("\n== Phase 3: delivery route ==")
    print(f"Stops to visit (graph nodes): {r['stops']}")
    print("Shortest distances from depot (Dijkstra): "
          + ", ".join(f"{s}:{r['dist'][0][s]}" for s in r["stops"]))
    print(f"Stop order (nearest-neighbour TSP): {' -> '.join(map(str, r['order']))}")
    print(f"Full road path: {' -> '.join(map(str, r['full_path']))}")
    print(f"Total route length: {r['length']} km")
    if len(r["stops"]) <= 8:
        _, opt = brute_force_tour(r["dist"], 0, r["stops"])
        print(f"Optimal tour (brute force): {opt} km -> heuristic is {r['length'] / opt:.2f}x optimal")

    print("\nRuntimes (ms): " + ", ".join(f"{k}={v * 1000:.3f}" for k, v in r["times"].items()))


if __name__ == "__main__":
    show(sys.argv[1] if len(sys.argv) > 1 else "data/small.json")
