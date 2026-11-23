import json
import random
import math

"""validate the matrix to make sure it's 2D and make sure it's a distance matrix (input must be list)"""
def validate_matrix(cities, matrix):
    # input should be a list
    if not isinstance(cities, list):
        raise ValueError("Invalid! cities must be 'list'.")
    if not isinstance(matrix, list):
        raise ValueError("Invalid! matrix must be 'list'.")
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
        if not isinstance(row, list):
            raise ValueError("Invalid! row must be 'list'.")
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

"""check the route to make sure it's a valid and perfect route then calculate the total distance"""
def route_distance(matrix, route):
    # check for duplicate routes
    if len(set(route)) != len(route):
        raise ValueError("Invalid! Duplicate cities in the route.")
    # check the route to make sure it has the same amount of cities to route to (missing cities)
    n = len(matrix)
    if len(route) != n:
        raise ValueError(f"Invalid! Route has {len(route)} cities, expected {n}")
    # index out of range
    if set(route) != set(range(n)):
        raise ValueError("Invalid! Route must contain each city index from 0 to n - 1.")

    # the distance calculation using the route given (return back to the starting position as well (e.g route = [0, 2, 1]) route from 0->2->1 then 1->0)
    distance = 0
    for k in range(len(route)):
        distance += matrix[route[k]][route[(k + 1) % len(route)]]

    return distance

"""load the dataset from JSON to python and validate it before returning the data"""
def load_dataset(path):
    # try opening the path and store the JSON object as python dict in data
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Error! Path: {path} not found.")
    except OSError as e:
        raise ValueError(f"Error! {e}")
    except json.JSONDecodeError:
        raise ValueError("Error! The File is not a valid JSON file.")

    # must be a dictionary and must have key of "cities" and "matrix"
    if not isinstance(data, dict):
        raise ValueError("Error! The file must contain a JSON object.")
    for key in ("cities", "matrix"):
        if key not in data:
            raise ValueError(f"Error! Key: {key!r} not found.")

    # unpack the data
    cities = data["cities"]
    matrix = data["matrix"]
    # validate the matrix and return it
    validate_matrix(cities, matrix)
    return cities, matrix

"""save the cities and matrix into the dataset JSON file"""
def save_dataset(path, cities, matrix):
    validate_matrix(cities, matrix)
    # we write the json file like this
    data = (
        "{\n"
        f' "cities": {json.dumps(cities)},\n'
        f' "matrix": {json.dumps(matrix)}, \n'
        "}\n"
    )
    # open the destination and write it
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
    except OSError as e:
        raise ValueError(f"Error! could not write to {path}: {e}")

def generate_dataset(n, seed=0):
    rng = random.Random(seed)

    

save_dataset("datasets/test.json", ["A", "B", "C", "D"], [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])

