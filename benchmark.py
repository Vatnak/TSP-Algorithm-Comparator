import argparse
import csv
import statistics
import time
from pathlib import Path

from data import load_dataset, generate_dataset, route_distance
from brute_force import brute_force
from nearest_neighbor import nearest_neighbor, nearest_neighbor_best_start

BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"
GRAPH_DIR = RESULTS_DIR / "graphs"

# Same limit as main.py. 10 cities = 9! = 362,880 routes, still fine in Python.
BRUTE_FORCE_LIMIT = 10
START_CITY = 0

# Very fast algorithms are repeated and averaged so the timer is not just noise.
NN_REPEATS = 200
NN_BEST_REPEATS = 20
BF_REPEATS = 3


def time_function(func, repeats):
    """Run func() several times. Return (result of last run, median seconds)."""
    times = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = func()
        times.append(time.perf_counter() - t0)
    return result, statistics.median(times)


def load_all_datasets(extra):
    """Return a list of (n, cities, matrix), sorted by n."""
    datasets = {}
    for path in DATASET_DIR.glob("*.json"):
        cities, matrix = load_dataset(str(path))
        datasets[len(cities)] = (cities, matrix)

    if extra:
        # Same generator as data.py, seed = n, so results are repeatable.
        for n in (4, 6, 7, 9):
            if n not in datasets:
                datasets[n] = generate_dataset(n, seed=n)

    return [(n, *datasets[n]) for n in sorted(datasets)]


def check_route(matrix, route, reported_total, label):
    """Make sure the route is valid and its distance is correct."""
    if route[0] != route[-1]:
        raise AssertionError(f"{label}: route does not return to the start")
    actual = route_distance(matrix, route[:-1])  # raises ValueError if invalid
    if abs(actual - reported_total) > 1e-6:
        raise AssertionError(
            f"{label}: reported {reported_total} but route is really {actual}"
        )


def run_benchmark(extra=False):
    rows = []
    for n, cities, matrix in load_all_datasets(extra):
        row = {"cities": n}

        # Nearest Neighbor (heuristic, O(n^2))
        (route, total), secs = time_function(
            lambda: nearest_neighbor(matrix, START_CITY), NN_REPEATS)
        check_route(matrix, route, total, f"NN n={n}")
        row["nn_distance"], row["nn_time"] = total, secs

        # Nearest Neighbor, best start city (O(n^3))
        (route, total), secs = time_function(
            lambda: nearest_neighbor_best_start(matrix), NN_BEST_REPEATS)
        check_route(matrix, route, total, f"NN best start n={n}")
        row["nn_best_distance"], row["nn_best_time"] = total, secs

        # Brute Force (exact, O(n!)), only when the dataset is small enough
        if n <= BRUTE_FORCE_LIMIT:
            repeats = BF_REPEATS if n <= 8 else 1
            (route, total), secs = time_function(
                lambda: brute_force(matrix, START_CITY), repeats)
            check_route(matrix, route, total, f"BF n={n}")
            row["bf_distance"], row["bf_time"] = total, secs
            row["nn_gap_pct"] = (row["nn_distance"] - total) / total * 100
            row["nn_best_gap_pct"] = (row["nn_best_distance"] - total) / total * 100
        else:
            row["bf_distance"] = row["bf_time"] = None
            row["nn_gap_pct"] = row["nn_best_gap_pct"] = None

        rows.append(row)
        print(f"  finished {n} cities")
    return rows


# ---------- output ----------

COLUMNS = [
    ("cities", "Cities"),
    ("bf_time", "BF time (s)"),
    ("nn_time", "NN time (s)"),
    ("nn_best_time", "NN best-start time (s)"),
    ("bf_distance", "BF distance"),
    ("nn_distance", "NN distance"),
    ("nn_best_distance", "NN best-start distance"),
    ("nn_gap_pct", "NN gap (%)"),
    ("nn_best_gap_pct", "NN best-start gap (%)"),
]


def fmt(key, value):
    if value is None:
        return "skipped"
    if key == "cities":
        return str(value)
    if key.endswith("_time"):
        return f"{value:.6f}"
    if key.endswith("_pct"):
        value = abs(value) if abs(value) < 1e-9 else value  # avoid printing -0.00
    return f"{value:.2f}"


def print_table(rows):
    headers = [h for _, h in COLUMNS]
    body = [[fmt(k, r[k]) for k, _ in COLUMNS] for r in rows]
    widths = [max(len(h), *(len(line[i]) for line in body)) for i, h in enumerate(headers)]
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print("\n" + line)
    print("-" * len(line))
    for b in body:
        print("  ".join(c.ljust(widths[i]) for i, c in enumerate(b)))
    print("\nBF = Brute Force, NN = Nearest Neighbor.")
    print("Gap = how much longer the NN route is than the optimal Brute Force route.")


def save_csv(rows):
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / "benchmark_results.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([h for _, h in COLUMNS])
        for r in rows:
            writer.writerow([fmt(k, r[k]) for k, _ in COLUMNS])
    print(f"\nSaved table: {path}")


def save_graphs(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")  # save to files, no window needed
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed, skipping graphs. Run: pip install -r requirments.txt")
        return

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    ns = [r["cities"] for r in rows]
    bf = [r for r in rows if r["bf_time"] is not None]

    # Graph 1: execution time (log scale because the gap is huge)
    plt.figure(figsize=(7, 4.5))
    plt.plot([r["cities"] for r in bf], [r["bf_time"] for r in bf],
             "o-", label="Brute Force (O(n!))")
    plt.plot(ns, [r["nn_time"] for r in rows], "s-", label="Nearest Neighbor (O(n²))")
    plt.plot(ns, [r["nn_best_time"] for r in rows], "^-", label="NN best start (O(n³))")
    plt.yscale("log")
    plt.xlabel("Number of cities")
    plt.ylabel("Execution time (seconds, log scale)")
    plt.title("Execution time vs number of cities")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "time_vs_cities.png", dpi=150)
    plt.close()

    # Graph 2: route distance on the sizes where Brute Force finished
    plt.figure(figsize=(7, 4.5))
    xs = range(len(bf))
    width = 0.27
    plt.bar([x - width for x in xs], [r["bf_distance"] for r in bf], width,
            label="Brute Force (optimal)")
    plt.bar(list(xs), [r["nn_distance"] for r in bf], width, label="Nearest Neighbor")
    plt.bar([x + width for x in xs], [r["nn_best_distance"] for r in bf], width,
            label="NN best start")
    plt.xticks(list(xs), [r["cities"] for r in bf])
    plt.xlabel("Number of cities")
    plt.ylabel("Total route distance")
    plt.title("Route quality (small datasets)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "distance_comparison.png", dpi=150)
    plt.close()

    # Graph 3: how far from optimal is Nearest Neighbor
    plt.figure(figsize=(7, 4.5))
    plt.plot([r["cities"] for r in bf], [r["nn_gap_pct"] for r in bf],
             "s-", label="Nearest Neighbor")
    plt.plot([r["cities"] for r in bf], [r["nn_best_gap_pct"] for r in bf],
             "^-", label="NN best start")
    plt.xlabel("Number of cities")
    plt.ylabel("Longer than optimal (%)")
    plt.title("Accuracy gap compared with Brute Force")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "accuracy_gap.png", dpi=150)
    plt.close()

    # Graph 4: Nearest Neighbor alone on all sizes (shows O(n²) growth)
    plt.figure(figsize=(7, 4.5))
    plt.plot(ns, [r["nn_time"] * 1000 for r in rows], "s-", label="Nearest Neighbor")
    plt.plot(ns, [r["nn_best_time"] * 1000 for r in rows], "^-", label="NN best start")
    plt.xlabel("Number of cities")
    plt.ylabel("Execution time (milliseconds)")
    plt.title("Nearest Neighbor on all dataset sizes")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "nn_time_all_sizes.png", dpi=150)
    plt.close()

    print(f"Saved graphs in: {GRAPH_DIR}")


def main():
    parser = argparse.ArgumentParser(description="TSP benchmark (Task 4)")
    parser.add_argument("--extra", action="store_true",
                        help="also test 4, 6, 7 and 9 cities")
    parser.add_argument("--no-graphs", action="store_true",
                        help="only print and save the table")
    args = parser.parse_args()

    print("Running benchmark (Brute Force on 10 cities may take a few seconds)...")
    rows = run_benchmark(extra=args.extra)
    print_table(rows)
    save_csv(rows)
    if not args.no_graphs:
        save_graphs(rows)


if __name__ == "__main__":
    main()