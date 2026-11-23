# TSP Algorithm Comparator

**COSC 251 – Data Structures | Fall 2026**

**American University of Phnom Penh (AUPP)**

**Group 3**

## 1. Project Overview

The **TSP Algorithm Comparator** is a Python-based academic project that implements and compares two algorithms for solving the Traveling Salesman Problem (TSP): **Brute Force** and **Nearest Neighbor**.

The Traveling Salesman Problem involves finding the shortest possible route that visits every city exactly once and returns to the starting city.

This project focuses on evaluating how the two algorithms differ in terms of:

- Total route distance
- Execution time
- Computational complexity
- Solution accuracy
- Performance with increasing numbers of cities

## 2. Project Objectives

1. Understand the Traveling Salesman Problem and its NP-hard classification.
2. Implement Brute Force and Nearest Neighbor algorithms in Python.
3. Represent cities and distances using a distance matrix.
4. Compare exact and heuristic algorithmic approaches.
5. Evaluate performance using different dataset sizes.
6. Analyze the advantages and limitations of both algorithms.

## 3. Algorithms

### Brute Force

Brute Force is an exact algorithm that examines all possible routes to determine the shortest one.

- **Time Complexity:** O(n!)
- **Advantage:** Guarantees the optimal solution.
- **Limitation:** Computationally expensive for large datasets.

### Nearest Neighbor

Nearest Neighbor is a greedy heuristic that repeatedly selects the closest unvisited city until all cities have been visited.

- **Time Complexity:** O(n²)
- **Advantage:** Faster and more practical for larger datasets.
- **Limitation:** Does not guarantee the optimal solution.

## 4. Technologies and Data Structures

- **Programming Language:** Python 3
- **Interface:** Command-Line Interface (CLI)
- **Data Structures:** Python lists and 2D distance matrices
- **Data Format:** JSON for prepared datasets
- **Version Control:** Git and GitHub

The project is designed to use Python's standard library where possible.

## 5. Project Structure

```text
tsp-algorithm-comparator/
│
├── main.py
├── data.py
├── brute_force.py
├── nearest_neighbor.py
├── benchmark.py
│
├── datasets/
├── tests/
├── results/
│   └── graphs/
├── docs/
│
├── README.md
├── requirements.txt
└── .gitignore
```

### File Descriptions

| File | Responsibility |
|---|---|
| `main.py` | Main program and command-line interface |
| `data.py` | Distance matrix, data loading, and validation |
| `brute_force.py` | Brute Force algorithm implementation |
| `nearest_neighbor.py` | Nearest Neighbor algorithm implementation |
|

## 6. Requirements
 
- Python 3.8 or newer
- The main program uses only the Python standard library, so nothing needs to be installed to run it.
- `matplotlib` is only needed for the graphs in the performance analysis:
```bash
pip install -r requirments.txt
```
 
## 7. How to Run
 
1. Download or clone the project and open the project folder in a terminal (or VS Code).
2. Make sure `main.py`, `data.py`, `brute_force.py`, `nearest_neighbor.py` and the `datasets/` folder are in the same folder.
3. Start the program:
```bash
python main.py
```
 
On macOS or Linux, use `python3 main.py` if `python` does not work.
 
## 8. Using the Program
 
The program is menu-driven. Type the number of an option and press Enter.
 
### Main menu
 
```text
1) Choose dataset
2) Run algorithm
3) Exit
```
 
### Step 1: Choose a dataset
 
| Option | Description |
|---|---|
| 1 | Prepared dataset: pick one of the JSON files in `datasets/` |
| 2 | Load a JSON file from a path you type |
| 3 | Enter city names and distances manually |
| 4 | Generate a random dataset (2 to 100 cities) |
 
### Step 2: Run an algorithm
 
| Option | Description |
|---|---|
| 1 | Brute Force (exact) |
| 2 | Nearest Neighbor (fast heuristic) |
| 3 | Nearest Neighbor- best start city|
| 4 | Compare Brute Force and Nearest Neighbor |
 
For options 1, 2 and 4, you also choose the start city from a numbered list.
 
### Output
 
For each run the program displays:
 
- The route (starting and ending at the start city)
- The total distance
- The execution time in seconds
- For option 4, how much longer the Nearest Neighbor route is compared with the optimal route
### Example session
 
```text
[No dataset loaded]
1) Choose dataset
2) Run algorithm
3) Exit
Choose: 1
1) Prepared dataset (datasets/ folder)
2) Load JSON file from a path
3) Enter cities and distances manually
4) Generate random dataset
Choose: 1          (prepared dataset)
  1) small_5.json
  2) small_8.json
  3) small_10.json
  4) large_20.json
  5) large_50.json
  6) large_100.json
Pick a file: 2     (small_8.json)
 
[Dataset loaded: 8 cities]
[Dataset loaded: 8 cities]
1) Choose dataset
2) Run algorithm
3) Exit
Choose: 2          (run algorithm)
1) Brute Force (exact)
2) Nearest Neighbor (fast heuristic)
3) Nearest Neighbor - best start city
4) Compare Brute Force and Nearest Neighbor
Choose: 4          (compare both)
Choose start city number: 1
 
Algorithm : Brute Force
Route     : City1 -> City6 -> City5 -> City4 -> City8 -> City3 -> City2 -> City7 -> City1
Distance  : 280.85
Time      :  0.004493 seconds
Algorithm : Nearest Neighbor
Route     : City1 -> City7 -> City2 -> City6 -> City5 -> City4 -> City8 -> City3 -> City1
Distance  : 294.71
Time      : 0.000023 seconds
Nearest Neighbor is 4.94% longer than the optimal route.
```
