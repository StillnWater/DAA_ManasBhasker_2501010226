# Mini-Courier Planner: Report
Course: Design & Analysis of Algorithms (ETCCDA302), Capstone Assignment

## 1. Problem design (Phase 1)
A courier van starts at a depot (graph node 0) with a weight limit. Many parcels are waiting; the
van can carry only some of them on one trip. We must decide **which parcels go first, which fit,
and in what order to drive**.

**Data design**
- Parcel: `id, dest (graph node), weight (integer kg), priority (1-5), deadline (hours)`.
- Knapsack value of a parcel = `priority*10 + max(0, 24 - deadline)`, so express and tight-deadline parcels are worth more.
- Road network: undirected weighted graph (weights = km), stored as an adjacency list. Datasets are JSON files in `data/`.

**Pipeline and why each algorithm was chosen**

| Step | Algorithm | Why | Complexity |
|---|---|---|---|
| Prioritise | Merge sort on (deadline, -priority, id) | Guaranteed O(n log n), stable | O(n log n) time, O(n) space |
| Choose parcels | 0/1 knapsack DP | A parcel is taken whole or not at all; greedy can be wrong, DP is exact | O(nW) time and space |
| Distances | Dijkstra with a binary heap | Roads have non-negative weights; stops are not directly connected | O((V+E) log V) per run |
| Route | Nearest-neighbour TSP | Exact TSP is O(k!) / NP-hard; greedy is fast | O(k^2) |

```
parcels --merge sort--> urgency order --knapsack DP--> parcels for this trip
   --> delivery stops --Dijkstra from depot + each stop--> distance table
   --nearest-neighbour--> stop order --expand with Dijkstra paths--> full road route
```

## 2. Prioritisation and packing (Phase 2)
Sample run (`data/small.json`, 10 parcels, 40 kg van; full trace in `results/small_run_output.txt`):
- Sorted order by urgency: parcels 8, 7, 3, 1, 4, 9, 10, 2, 6, 5.
- DP result: parcels **[8, 7, 3, 4, 2, 6]**, total weight **37/40 kg**, total value **289**.
- Left for the next trip: [1, 9, 10, 5].
- The program prints the DP table (every 5 kg column) as evidence. Tests confirm the DP value equals the best subset found by brute force on 20 random instances.

## 3. Route planning (Phase 3)
For the small run the stops are nodes [1, 2, 8, 11]. Dijkstra distances from the depot: 1:11, 2:23, 8:1, 11:7.
- Stop order: 0 -> 8 -> 11 -> 1 -> 2 -> 0
- Total route length: **62 km**
- Full road path (through junctions): 0 -> 8 -> 10 -> 7 -> 11 -> 7 -> 10 -> 1 -> 10 -> 7 -> 2 -> 7 -> 10 -> 8 -> 0
- Brute-force optimum: 60 km, so the heuristic was 1.03x optimal here.

Dijkstra was verified against Floyd-Warshall on 10 random graphs; the heuristic route was never shorter than the brute-force optimum in tests (as it must be).

## 4. Performance testing (Phase 4)
Measured with `time.perf_counter`, best of 2-3 runs (`results/benchmark_output.txt`, `results/runtimes.csv`). Times in ms; your machine will give different numbers but the same trends.

**Sorting** (charts: `results/chart_sorting.png`)

| n | Merge | Quick | Insertion | Python `sorted` |
|---|---|---|---|---|
| 100 | 0.19 | 0.27 | 0.34 | 0.02 |
| 1000 | 2.75 | 4.38 | 23.19 | 0.19 |
| 4000 | 8.20 | 20.42 | 378.72 | 0.97 |

Insertion sort grows roughly with n^2 (n x4 from 1000 to 4000 gives about 16x); merge sort grows close to n log n. Built-in `sorted` is fastest because it is written in C.

**Knapsack:** 0.81 ms (n=100) to 35.6 ms (n=4000) at W=100; 3.5 ms (W=50) to 78.7 ms (W=800) at n=1000. Time grows about linearly in both n and W, matching O(nW) (`chart_knapsack_n.png`, `chart_knapsack_w.png`).

**Dijkstra** (one source, E = 3V): 0.07 ms at V=100 to 6.9 ms at V=4000 (`chart_dijkstra.png`).

**Nearest neighbour:** 0.008 ms for 10 stops to 7.0 ms for 399 stops, roughly quadratic (`chart_tsp.png`).

**End-to-end** (`chart_end_to_end.png`), ms:

| Dataset | Sort | Knapsack | Dijkstra | TSP |
|---|---|---|---|---|
| small (10 parcels) | 0.01 | 0.03 | 0.04 | 0.00 |
| medium (100) | 0.14 | 0.65 | 0.84 | 0.04 |
| large (1000) | 1.72 | 7.97 | 14.59 | 0.38 |

**Where the time goes:** on larger inputs Dijkstra (one run per stop) and the knapsack table dominate; sorting and the TSP step are small.

**Suggested optimisations**
- Use a 1-D knapsack array if only the value is needed (cuts memory from O(nW) to O(W)); keep the table only when the chosen parcels must be traced back.
- Run Dijkstra only from stops, not all nodes (already done), and stop early once all stops are settled.
- Improve the route with 2-opt after nearest neighbour; use Christofides if a guaranteed 1.5x bound is needed.
- Cache the distance table between trips when the road network does not change.
- Plan several trips by repeating knapsack on the parcels left over.

## 5. Result explanation and limitations (Phase 5)
Screenshots/output traces are in `results/` (`small_run_output.txt`, `medium_run_output.txt`, `test_output.txt`, and the PNG charts).

Honest limits:
- Nearest neighbour has no fixed quality guarantee (here 1.03x optimal on one small case only; it was not measured on larger sets).
- Deadlines affect parcel *selection* through the value formula and the sort order, but the route itself ignores per-parcel deadlines.
- The knapsack handles one capacity (weight only), not volume.
- The road graph is randomly generated, not real map data.
- Benchmark numbers depend on the machine.
