
"""validate the matrix to make sure it's 2D and make sure it's a distance matrix"""
def validate_matrix(cities, matrix):
    # must have at least 2 cities
    if len(cities) <= 1:
        raise ValueError(f"Only {len(cities)} city! There is no route to find.")
    # check if the number of rows in the matrix match the number of cities
    if len(cities) != len(matrix):
        raise ValueError(f"Invalid! Matrix has {len(matrix)} rows, but there are {len(cities)} cities.")
    # check for duplicate cities name
    if len(set(cities)) != len(cities):
        raise ValueError("Invalid! Duplicate cities name.")

    # check each rows of the matrix to make sure they have the same length as the cities
    for i, row in enumerate(matrix):
        if len(row) != len(cities):
            raise ValueError(f"Invalid! Row {i} has {len(row)} values. expected {len(cities)}.")
            
        # check to make sure every cells must be a number
        for j, value in enumerate(row):
            if not isinstance(value, (int, float)):
                raise ValueError(f"Invalid! Row {i}, column {j}: {value!r} is not a number.")
            # make sure it's must be positive numbers
            elif value < 0:
                raise ValueError(f"Invalid Row {i}, column {j}: ({value}) is a negative number.")
            # make sure it must be zero diagonal matrix because it is a distance matrix
            elif i == j and value != 0:
                raise ValueError(f"Invalid Row {i}: the distance from the city to itself must be 0, but got ({value}).")
                
    # check that the matrix is symmetric (distance A to B must be equals B to A)
    n = len(cities)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Invalid! Distance from city {i} to {j} ({matrix[i][j]}) differs from {j} to {i} ({matrix[j][i]}).")
                
    return True

"""check the route to make sure it's all perfect and cool then calculate the total distance"""
def route_distance(matrix, route):
    # check for duplicate routes
    if len(set(route)) != len(route):
        raise ValueError("Invalid! Duplicate cities in the route.")
    # check the route to make sure it has the same amount of cities to route to (missing cities)
    n = len(matrix)
    if len(route) != n:
        raise ValueError(f"Invalid! Route has {len(route)} cities, expected {n}")
    # index out of range
    if set(route) != set(range(len(route))):
        raise ValueError(f"Invalid! Route must contain each city index from 0 to n - 1.")
    
    distance = 0
    for k in range(len(route)):
        distance += matrix[route[k]][route[(k + 1) % len(route)]]

    return distance

matrix = [[0, 10, 15, 20],
          [10, 0, 35, 25],
          [15, 35, 0, 30],
          [20, 25, 30, 0]]

print(route_distance(matrix, [0, 1, 2, -1]))  
print(route_distance(matrix, [0, 1, 3, 2]))   
print(validate_matrix(["A", "B", "C"], [[0, 5, 2], [5, 0, 3], [2, 3, 0]]))
print(route_distance([[0, 10, 15], [10, 0, 35], [15, 35, 0]], [0, 2, 1]))
