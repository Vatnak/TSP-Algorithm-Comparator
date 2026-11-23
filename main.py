
import time
from pathlib import Path

from data import load_dataset, validate_matrix, generate_dataset, save_dataset
from brute_force import brute_force
from nearest_neighbor import nearest_neighbor, nearest_neighbor_best_start

BRUTE_FORCE_LIMIT = 10 
DATASET_DIR = Path(__file__).parent / "datasets"


def ask_int(prompt, low, high):
    """Keep asking until the user enters a whole number in [low, high]."""
    while True:
        try:
            value = int(input(prompt).strip())
            if low <= value <= high:
                return value
        except ValueError:
            pass
        print(f"  Please enter a whole number from {low} to {high}.")


def ask_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value >= 0:
                return value
        except ValueError:
            pass
        print("  Please enter a non-negative number.")


def enter_manually():
    n = ask_int("Number of cities (2-100): ", 2, 100)
    cities = []
    while len(cities) < n:
        name = input(f"  Name of city {len(cities) + 1}: ").strip()
        if not name or name in cities:
            print("  Name must be non-empty and unique.")
            continue
        cities.append(name)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = ask_float(f"  Distance {cities[i]} <-> {cities[j]}: ")
            matrix[i][j] = matrix[j][i] = d
    validate_matrix(cities, matrix)
    return cities, matrix


def choose_dataset():
    print("\n1) Prepared dataset (datasets/ folder)")
    print("2) Load JSON file from a path")
    print("3) Enter cities and distances manually")
    print("4) Generate random dataset")
    choice = ask_int("Choose: ", 1, 4)
    try:
        if choice == 1:
            files = sorted(DATASET_DIR.glob("*.json"),
                           key=lambda p: int(p.stem.split("_")[-1]) if p.stem.split("_")[-1].isdigit() else 0)
            if not files:
                print("  No datasets found in the datasets/ folder.")
                return None
            for i, f in enumerate(files, 1):
                print(f"  {i}) {f.name}")
            return load_dataset(str(files[ask_int("Pick a file: ", 1, len(files)) - 1]))
        if choice == 2:
            return load_dataset(input("Path to JSON file: ").strip().strip('"'))
        if choice == 3:
            return enter_manually()
        n = ask_int("Number of cities (2-100): ", 2, 100)
        return generate_dataset(n, seed=int(time.time()))
    except (ValueError, OSError) as e:
        print(f"  Error: {e}")
        return None


def show_result(label, cities, route, total, elapsed):
    # both algorithms already return the route ending at the start city
    print(f"\nAlgorithm : {label}")
    print("Route     : " + " -> ".join(cities[i] for i in route))
    print(f"Distance  : {total:.2f}")
    print(f"Time      : {elapsed:.6f} seconds")


def run_algorithm(cities, matrix):
    n = len(cities)
    print("\n1) Brute Force (exact)")
    print("2) Nearest Neighbor (fast heuristic)")
    print("3) Nearest Neighbor - best start city")
    print("4) Compare Brute Force and Nearest Neighbor")
    choice = ask_int("Choose: ", 1, 4)

    if choice in (1, 4) and n > BRUTE_FORCE_LIMIT:
        print(f"  Brute Force is too slow for {n} cities (limit {BRUTE_FORCE_LIMIT}).")
        print("  Use Nearest Neighbor for this dataset.")
        return

    start = 0
    if choice != 3:
        print("  Start city:")
        for i, c in enumerate(cities):
            print(f"    {i + 1}) {c}")
        start = ask_int("  Choose start city number: ", 1, n) - 1

    jobs = {
        1: [("Brute Force", lambda: brute_force(matrix, start))],
        2: [("Nearest Neighbor", lambda: nearest_neighbor(matrix, start))],
        3: [("Nearest Neighbor (best start)", lambda: nearest_neighbor_best_start(matrix))],
        4: [("Brute Force", lambda: brute_force(matrix, start)),
            ("Nearest Neighbor", lambda: nearest_neighbor(matrix, start))],
    }[choice]

    results = []
    for label, func in jobs:
        t0 = time.perf_counter()
        try:
            route, total = func()
        except Exception as e:
            print(f"  {label} failed: {e}")
            return
        elapsed = time.perf_counter() - t0
        show_result(label, cities, route, total, elapsed)
        results.append((total, elapsed))

    if choice == 4:
        (bf, _), (nn, _) = results
        gap = (nn - bf) / bf * 100 if bf else 0
        print(f"\nNearest Neighbor is {gap:.2f}% longer than the optimal route.")


def main():
    print("=== TSP Algorithm Comparator (COSC 251, Group 3) ===")
    data = None
    while True:
        print(f"\n[Dataset loaded: {len(data[0])} cities]" if data else "\n[No dataset loaded]")
        print("1) Choose dataset\n2) Run algorithm\n3) Exit")
        choice = ask_int("Choose: ", 1, 3)
        if choice == 1:
            data = choose_dataset() or data
        elif choice == 2:
            if data is None:
                print("  Load a dataset first.")
            else:
                run_algorithm(*data)
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Goodbye!")
