from itertools import permutations


def brute_force(matrix, start_city):
    # Collect the cities to visit, excluding the starting city.
    cities = []

    for city in range(len(matrix)):
        if city != start_city:
            cities.append(city)

    best_route = None
    shortest_distance = float("inf")

    # Check every possible visiting order.
    for order in permutations(cities):
        route = [start_city] + list(order) + [start_city]

        # Calculate the route distance using the matrix.
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += matrix[route[i]][route[i + 1]]

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            best_route = route
    return best_route, shortest_distance

