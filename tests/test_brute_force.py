import sys
from pathlib import Path

# Find brute_force.py when this test is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from brute_force import brute_force


def test_four_cities():
    matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]

    route, total_distance = brute_force(matrix, 0)

    assert total_distance == 80
    assert route[0] == 0
    assert route[-1] == 0
    # Before returning home, visit each city exactly once.
    assert sorted(route[:-1]) == [0, 1, 2, 3]


def check_equal_distances(city_count, start_city):
    # Each move to a different city costs 10.
    matrix = []
    for city in range(city_count):
        row = []
        for other_city in range(city_count):
            if city == other_city:
                row.append(0)
            else:
                row.append(10)
        matrix.append(row)

    route, total_distance = brute_force(matrix, start_city)

    # A complete trip has one move per city, including the return home.
    assert total_distance == city_count * 10
    assert route[0] == start_city
    assert route[-1] == start_city
    assert sorted(route[:-1]) == list(range(city_count))

    # Check that the reported distance matches the returned route.
    route_distance = 0
    for i in range(len(route) - 1):
        route_distance += matrix[route[i]][route[i + 1]]
    assert route_distance == total_distance


def test_five_cities():
    check_equal_distances(5, 0)


def test_eight_cities():
    check_equal_distances(8, 0)


def test_ten_cities():
    check_equal_distances(10, 0)


def test_different_start_city():
    check_equal_distances(5, 2)


if __name__ == "__main__":
    test_four_cities()
    print("4-city test passed.")
    test_five_cities()
    print("5-city test passed.")
    test_eight_cities()
    print("8-city test passed.")
    test_ten_cities()
    print("10-city test passed.")
    test_different_start_city()
    print("Different starting city test passed.")
