
def validate_matrix(cities, matrix):
    # must have at least 2 cities
    if len(cities) <= 1:
        raise ValueError(f"Only {len(cities)} city! There is no route to find.")
    # check if the number of rows in the matrix match the number of cities
    if len(cities) != len(matrix):
        raise ValueError(f"Invalid! Matrix has {len(matrix)} rows, but there are {len(cities)} cities.")

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

    return True
    
print(validate_matrix(["A"], [[0]]))
