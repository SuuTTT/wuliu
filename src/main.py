import os
import datetime
import argparse
from util import generate_test_data_json, save_test_data, load_test_data, json_to_matrices, save_results
from allocation import brute_force_allocation

# Setup argparse for command-line arguments
parser = argparse.ArgumentParser(description='Generate and process test data.')

parser.add_argument('--num_orders', type=int, default=2, help='Number of orders.')
parser.add_argument('--num_warehouses', type=int, default=2, help='Number of warehouses.')
parser.add_argument('--max_demand', type=int, default=5, help='Maximum demand.')
parser.add_argument('--max_inventory', type=int, default=3, help='Maximum inventory.')
parser.add_argument('--exceed_inventory', action='store_true', help='Flag to indicate if demand can exceed inventory.')

args = parser.parse_args()

# Ensure the directory exists or create it
directory = "data_gen"
if not os.path.exists(directory):
    os.makedirs(directory)

# Generate and save test data
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = os.path.join(directory, f"test_data_{timestamp}.json")

test_data, X, Y, Z, priority_order = generate_test_data_json(args.num_orders, args.num_warehouses, args.max_demand, args.max_inventory, args.exceed_inventory)
save_test_data(filename, test_data)

# Load and process the test data
loaded_data = load_test_data(filename)
A1, A2, A3, order_list, warehouse_list, goods_dict = json_to_matrices(loaded_data)
allocation_matrix, max_transport_time = brute_force_allocation(A1, A2, A3, priority_order)

# Display results
print("Allocation Matrix:\n", allocation_matrix)
print("\nMax Transport Time:", max_transport_time)


# Save results to file
results_filename = filename.replace("test_data", "results")
save_results(results_filename, allocation_matrix, max_transport_time)

# Display results
print("Allocation Matrix:\n", allocation_matrix)
print("\nMax Transport Time:", max_transport_time)