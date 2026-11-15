# Mini-Courier Planner (DAA Capstone, ETCCDA302)

Given parcels and a road network, the program (1) sorts parcels by urgency, (2) picks the most
valuable set that fits the van using knapsack DP, (3) finds shortest paths with Dijkstra, and
(4) orders the stops with a nearest-neighbour TSP heuristic. Python 3 only; `matplotlib` is needed
for the charts (`pip install matplotlib`). Everything else is the standard library.

## Execution steps
    python make_datasets.py        # (re)creates data/small.json, medium.json, large.json
    python main.py                 # demo on data/small.json (prints DP table, route, runtimes)
    python main.py data/medium.json
    python tests.py                # correctness checks (brute force / Floyd-Warshall comparisons)
    python benchmark.py            # runtimes + charts into results/

## Layout
| Path | Purpose | Phase |
|---|---|---|
| `courier/models.py`, `courier/datagen.py` | Parcel design, dataset generate/load | 1 |
| `courier/sorting.py` | Merge sort (chosen), insertion and quick sort (for comparison) | 2 |
| `courier/knapsack.py` | 0/1 knapsack DP with traceback | 2 |
| `courier/graph.py` | Graph, Dijkstra, path rebuild, random graph | 3 |
| `courier/tsp.py` | Nearest neighbour + brute-force optimum for tiny cases | 3 |
| `courier/planner.py` | Pipeline that joins all steps and times each one | all |
| `benchmark.py`, `results/` | Runtime tests, charts, CSV, saved console output | 4, 5 |
| `REPORT.md` | Design, results, analysis | 1, 4, 5 |

Dataset format (JSON): `capacity`, `nodes` (node 0 = depot), `edges` as `[u, v, km]`, and
`parcels` with `id, dest, weight, priority, deadline`.
