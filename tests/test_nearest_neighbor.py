"""Run from the project root with:  python -m unittest discover tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from nearest_neighbor import nearest_neighbor, nearest_neighbor_best_start


class TestNearestNeighbor(unittest.TestCase):
    # Classic 4-city example; optimal tour length is 80
    M4 = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]

    def test_small_known_result(self):
        # Verified by hand: 0->1 (10), 1->3 (25), 3->2 (30), 2->0 (15) = 80
        route, total = nearest_neighbor(self.M4, 0)
        self.assertEqual(route, [0, 1, 3, 2, 0])
        self.assertEqual(total, 80)

    def test_visits_every_city_once(self):
        route, _ = nearest_neighbor(self.M4, 0)
        self.assertEqual(sorted(route[:-1]), [0, 1, 2, 3])
        self.assertEqual(route[0], route[-1])

    def test_single_city(self):
        route, total = nearest_neighbor([[0]], 0)
        self.assertEqual(route, [0, 0])
        self.assertEqual(total, 0)

    def test_different_start(self):
        route, total = nearest_neighbor(self.M4, 2)
        self.assertEqual(route[0], 2)
        self.assertEqual(route[-1], 2)
        self.assertEqual(len(route), 5)

    def test_nn_is_not_always_optimal(self):
        # 5-city case where greedy is strictly worse than the best tour.
        # NN from 0 gives 40, but the optimal tour is 30 (checked by brute force).
        m = [
            [0, 4, 16, 1, 13],
            [4, 0, 14, 20, 1],
            [16, 14, 0, 15, 9],
            [1, 20, 15, 0, 8],
            [13, 1, 9, 8, 0],
        ]
        _, nn_total = nearest_neighbor(m, 0)
        self.assertEqual(nn_total, 40)
        self.assertGreater(nn_total, 30)

    def test_best_start_not_worse_than_single_start(self):
        _, single = nearest_neighbor(self.M4, 0)
        _, best = nearest_neighbor_best_start(self.M4)
        self.assertLessEqual(best, single)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            nearest_neighbor([], 0)
        with self.assertRaises(ValueError):
            nearest_neighbor(self.M4, 9)


if __name__ == "__main__":
    unittest.main()
