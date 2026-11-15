"""Phase 4: runtime tests on growing inputs. Writes charts + a CSV into results/."""
import csv
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from courier.datagen import random_parcels, make_dataset
from courier.sorting import merge_sort, insertion_sort, quick_sort, parcel_key
from courier.knapsack import knapsack
from courier.graph import random_graph, dijkstra
from courier.tsp import nearest_neighbor
from courier.planner import plan


def timeit(fn, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        s = time.perf_counter(); fn(); best = min(best, time.perf_counter() - s)
    return best * 1000  # ms


def chart(x, series, title, xlabel, fname, logy=False):
    plt.figure(figsize=(6.5, 4))
    for label, ys in series.items():
        plt.plot(x, ys, marker="o", label=label)
    plt.title(title); plt.xlabel(xlabel); plt.ylabel("time (ms)")
    if logy: plt.yscale("log")
    plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig(f"results/{fname}", dpi=130); plt.close()


rows = []

# 1. Sorting algorithms
sizes = [100, 500, 1000, 2000, 4000]
s = {"Merge sort": [], "Quick sort": [], "Insertion sort": [], "Python sorted()": []}
for n in sizes:
    ps = random_parcels(n, 50, seed=n)
    s["Merge sort"].append(timeit(lambda: merge_sort(ps, parcel_key)))
    s["Quick sort"].append(timeit(lambda: quick_sort(ps, parcel_key)))
    s["Insertion sort"].append(timeit(lambda: insertion_sort(ps, parcel_key)))
    s["Python sorted()"].append(timeit(lambda: sorted(ps, key=parcel_key)))
chart(sizes, s, "Parcel sorting: runtime vs number of parcels", "parcels (n)", "chart_sorting.png", logy=True)
for k, v in s.items():
    rows += [("sorting", k, n, round(t, 4)) for n, t in zip(sizes, v)]

# 2. Knapsack DP (O(nW)): vary n, then vary capacity W
ks_n = [100, 500, 1000, 2000, 4000]
ks_n_t = [timeit(lambda: knapsack(random_parcels(n, 50, n), 100), 2) for n in ks_n]
caps = [50, 100, 200, 400, 800]
ps1000 = random_parcels(1000, 50, 1)
ks_w_t = [timeit(lambda: knapsack(ps1000, w), 2) for w in caps]
chart(ks_n, {"W = 100": ks_n_t}, "Knapsack DP: runtime vs parcels", "parcels (n)", "chart_knapsack_n.png")
chart(caps, {"n = 1000": ks_w_t}, "Knapsack DP: runtime vs capacity", "capacity W (kg)", "chart_knapsack_w.png")
rows += [("knapsack_n", "W=100", n, round(t, 4)) for n, t in zip(ks_n, ks_n_t)]
rows += [("knapsack_W", "n=1000", w, round(t, 4)) for w, t in zip(caps, ks_w_t)]

# 3. Dijkstra single run vs graph size
vs = [100, 500, 1000, 2000, 4000]
dj = []
for v in vs:
    g = random_graph(v, v * 2, seed=v)
    dj.append(timeit(lambda: dijkstra(g, 0)))
chart(vs, {"Dijkstra (1 source, E = 3V)": dj}, "Dijkstra: runtime vs graph size", "nodes (V)", "chart_dijkstra.png")
rows += [("dijkstra", "1 source", v, round(t, 4)) for v, t in zip(vs, dj)]

# 4. Nearest neighbour TSP vs number of stops (distance matrix pre-computed)
g = random_graph(400, 800, seed=7)
ks = [10, 25, 50, 100, 200, 399]
tsp_t = []
for k in ks:
    stops = list(range(1, k + 1))
    dist = {u: dijkstra(g, u)[0] for u in [0] + stops}
    tsp_t.append(timeit(lambda: nearest_neighbor(dist, 0, stops)))
chart(ks, {"Nearest neighbour": tsp_t}, "TSP heuristic: runtime vs stops", "stops (k)", "chart_tsp.png")
rows += [("tsp", "nearest_neighbor", k, round(t, 4)) for k, t in zip(ks, tsp_t)]

# 5. End to end on the three datasets: where does the time go?
import json
steps = ["sort", "knapsack", "dijkstra", "tsp"]
cfgs = [("small", 10, 12, 40, 1), ("medium", 100, 60, 100, 2), ("large", 1000, 300, 100, 3)]
stack = {k: [] for k in steps}
for name, n, nodes, cap, seed in cfgs:
    p, g, c = make_dataset(n, nodes, cap, seed)
    best = None
    for _ in range(3):
        t = plan(p, g, c)["times"]
        best = t if best is None or sum(t.values()) < sum(best.values()) else best
    for k in steps:
        stack[k].append(best[k] * 1000)
        rows.append(("end_to_end", k, name, round(best[k] * 1000, 4)))
plt.figure(figsize=(6.5, 4)); bottom = [0] * 3
for k in steps:
    plt.bar([c[0] for c in cfgs], stack[k], bottom=bottom, label=k)
    bottom = [b + v for b, v in zip(bottom, stack[k])]
plt.title("End-to-end runtime by step"); plt.ylabel("time (ms)"); plt.legend(); plt.tight_layout()
plt.savefig("results/chart_end_to_end.png", dpi=130); plt.close()

with open("results/runtimes.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["experiment", "series", "x", "time_ms"]); w.writerows(rows)

print("Sorting (ms):"); print("  n:", sizes)
for k, v in s.items(): print(f"  {k:16}", [round(x, 2) for x in v])
print("Knapsack vs n (ms):", [round(x, 2) for x in ks_n_t])
print("Knapsack vs W (ms):", [round(x, 2) for x in ks_w_t])
print("Dijkstra vs V (ms):", [round(x, 2) for x in dj])
print("TSP vs stops (ms):", [round(x, 3) for x in tsp_t])
print("End-to-end (ms) [sort, knapsack, dijkstra, tsp]:")
for i, c in enumerate(cfgs):
    print(f"  {c[0]:7}", [round(stack[k][i], 2) for k in steps])
