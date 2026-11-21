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