# filename: test_SA_solution_generation.py

import unittest
from optimizer import *
from util import *

class TestSolutionGeneration(unittest.TestCase):

    def test_gen_neighbour(self):
        orders = read_orders_from_file('orders_data2.json')
        initial_solution = generate_initial_solution(orders)
        warehouse_schedules = generate_warehouse_schedules(initial_solution)
        neighbor = get_neighbor(initial_solution, orders, warehouse_schedules)
        self.assertIsNotNone(neighbor)

    def test_generate_initial_solution(self):
        orders = read_orders_from_file('orders_data2.json')
        solution = generate_initial_solution(orders)
        #self.assertEqual(len(solution), len(orders))
        for sol in solution:
            self.assertIn('cknm', sol)
            self.assertIn('ksbysj', sol)
            self.assertIn('jsbysj', sol)

    def test_initial_solution_2(self):
        orders = read_orders_from_file('orders_data.json')
        initial_solution = generate_initial_solution(orders)
        #self.assertEqual(len(initial_solution), len(orders))
        for strategy in initial_solution:
            self.assertIn('cknm', strategy)

if __name__ == "__main__":
    unittest.main()
