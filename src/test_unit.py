# filename: test_SA_solution_generation.py

import unittest
from optimizer import *
from util import *

class TestSolutionGeneration(unittest.TestCase):



    def test_initial_solution_2(self):
        orders = read_orders_from_file('orders_data.json')
        initial_solution = generate_initial_solution(orders)
        #self.assertEqual(len(initial_solution), len(orders))
        for strategy in initial_solution:
            self.assertIn('cknm', strategy)

    def test_order_to_strategy(self):
        orders = read_orders_from_file('orders_data.json')
        
        
if __name__ == "__main__":
    unittest.main()
