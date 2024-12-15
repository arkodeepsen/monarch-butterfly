# test_mbo_core.py

import unittest
from mbo_core import generate_random_solution, fitness, repair

class TestMBOCore(unittest.TestCase):
    
    def test_generate_random_solution(self):
        num_items = 10
        solution = generate_random_solution(num_items)
        self.assertEqual(len(solution), num_items)
        for bit in solution:
            self.assertIn(bit, [0, 1])
    
    def test_fitness_feasible(self):
        solution = [1, 0, 1]
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50
        self.assertEqual(fitness(solution, values, weights, capacity), 180)
    
    def test_fitness_infeasible(self):
        solution = [1, 1, 1]
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50
        self.assertEqual(fitness(solution, values, weights, capacity), 0)
    
    def test_repair_feasible(self):
        solution = [1, 0, 1]
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50
        repaired = repair(solution, weights, capacity, values)
        self.assertEqual(repaired, solution)  # Already feasible
    
    def test_repair_infeasible(self):
        solution = [1, 1, 1]
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50
        repaired = repair(solution, weights, capacity, values)
        self.assertTrue(sum(w for w, bit in zip(weights, repaired) if bit) <= capacity)
        # Optimal repair would remove the item with lowest value-to-weight ratio first
        # In this case, item 3: 120/30 = 4, item 2: 100/20 = 5, item 1: 60/10 = 6
        # So item 3 is removed first to make it feasible
        expected_solution = [1, 1, 0]
        self.assertEqual(repaired, expected_solution)

if __name__ == '__main__':
    unittest.main()
