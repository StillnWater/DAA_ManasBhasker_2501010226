"""Create the sample datasets in data/."""
from courier.datagen import make_dataset, save_dataset

for name, (n_parcels, n_nodes, cap, seed) in {
    "small": (10, 12, 40, 1),
    "medium": (100, 60, 100, 2),
    "large": (1000, 300, 100, 3),
}.items():
    p, g, c = make_dataset(n_parcels, n_nodes, cap, seed)
    save_dataset(f"data/{name}.json", p, g, c)
    print("wrote", name)
