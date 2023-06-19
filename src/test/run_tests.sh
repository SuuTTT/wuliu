#!/bin/bash

echo "Starting Unit Tests..."
python -m unittest test_SA_init.py
python -m unittest test_SA_gen_neighbour.py
python -m unittest test_SA_init_with_conflict.py
echo "Unit Tests Completed."

echo "Starting Integration Tests..."
python -m unittest test_SA_full_process.py
echo "Integration Tests Completed."

echo "Starting System Tests..."
python -m unittest test_SA_system_large_orders.py
echo "System Tests Completed."

echo "Starting Performance Tests..."
python -m unittest test_SA_performance_runtime.py
python -m unittest test_SA_performance_resources.py
echo "Performance Tests Completed."
