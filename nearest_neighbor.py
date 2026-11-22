"""
nearest_neighbor.py
-------------------
Nearest Neighbor heuristic for the Traveling Salesman Problem (TSP).

How it works (greedy):
    1. Start at a chosen city and mark it as visited.
    2. Look at every UNVISITED city and pick the one closest to where we are now.
    3. Move there, mark it visited.
    4. Repeat step 2-3 until all cities are visited.
    5. Return to the starting city to close the tour.

Time complexity : O(n^2)  - n steps, and each step scans up to n cities.
Space complexity: O(n)    - one visited list + the route list.
Type of solution: HEURISTIC (fast, but NOT guaranteed to be optimal).
"""

import time


def nearest_neighbor(distance_matrix, start=0):
    """Run Nearest Neighbor from one starting city.

    Args:
        distance_matrix: n x n list of lists of distances.
        start: index of the city to start (and end) at. Default 0.

    Returns:
        (route, total_distance)
        route: list of city indices, starting AND ending at `start`
               e.g. [0, 2, 1, 3, 0]
        total_distance: length of the full round trip (including return).
    """
    n = len(distance_matrix)

    if n == 0:
        raise ValueError("Distance matrix is empty.")
    if not 0 <= start < n:
        raise ValueError(f"Start city {start} is out of range (0 to {n - 1}).")

    # Track visited / unvisited cities
    visited = [False] * n
    visited[start] = True

    route = [start]
    total_distance = 0
    current = start

    # We need to pick n - 1 more cities
    for _ in range(n - 1):
        nearest_city = None
        nearest_dist = float("inf")

        # Scan every unvisited city, keep the closest one
        for city in range(n):
            if not visited[city] and distance_matrix[current][city] < nearest_dist:
                nearest_dist = distance_matrix[current][city]
                nearest_city = city

        # Move to that city
        visited[nearest_city] = True
        route.append(nearest_city)
        total_distance += nearest_dist
        current = nearest_city

    # Return to the start to complete the tour
    total_distance += distance_matrix[current][start]
    route.append(start)

    return route, total_distance


def nearest_neighbor_best_start(distance_matrix):
    """Optional improvement: run Nearest Neighbor from EVERY city and keep
    the best tour. Costs O(n^3) but usually gives a shorter route.

    Returns:
        (route, total_distance)
    """
    best_route, best_distance = None, float("inf")
    for start in range(len(distance_matrix)):
        route, dist = nearest_neighbor(distance_matrix, start)
        if dist < best_distance:
            best_route, best_distance = route, dist
    return best_route, best_distance


def solve(distance_matrix, start=0):
    """Convenience wrapper for main.py / benchmark.py.

    Returns:
        (route, total_distance, elapsed_seconds)
    """
    t0 = time.perf_counter()
    route, total = nearest_neighbor(distance_matrix, start)
    elapsed = time.perf_counter() - t0
    return route, total, elapsed


if __name__ == "__main__":
    # Quick demo: run `python nearest_neighbor.py`
    demo = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    route, total, secs = solve(demo)
    print("Route:", " -> ".join(map(str, route)))
    print("Total distance:", total)
    print(f"Time: {secs:.8f} s")
