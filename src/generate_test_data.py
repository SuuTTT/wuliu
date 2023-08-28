import os
import datetime
import argparse
from util import generate_test_data_json, save_test_data, load_test_data, json_to_matrices, save_results
from allocation import brute_force_allocation

def generate_and_process_test_data(args):
    # Ensure the directory exists or create it
    directory = "data_gen"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate and save test data
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(directory, f"test_data_o{args.num_orders}_w{args.num_warehouses}_d{args.max_demand}_i{args.max_inventory}_{'exceed' if args.exceed_inventory else 'noexceed'}_{timestamp}.json")

    test_data, X, Y, Z, priority_order = generate_test_data_json(args.num_orders, args.num_warehouses, args.max_demand, args.max_inventory, args.exceed_inventory)
    save_test_data(filename, test_data)

    # Load and process the test data
    loaded_data = load_test_data(filename)
    A1, A2, A3, order_list, warehouse_list, goods_dict = json_to_matrices(loaded_data)
    allocation_matrix, max_transport_time = brute_force_allocation(A1, A2, A3, priority_order)

    # Save results to file
    results_filename = filename.replace("test_data", "results")
    save_results(results_filename, allocation_matrix, max_transport_time)

    # Display results
    print(f"Test case: o{args.num_orders}_w{args.num_warehouses}_d{args.max_demand}_i{args.max_inventory}_{'exceed' if args.exceed_inventory else 'noexceed'}")
    print("Allocation Matrix:\n", allocation_matrix)
    print("Max Transport Time:", max_transport_time)

def run_test_cases():
    # Baseline Test
    print("Running baseline test...")
    generate_and_process_test_data(argparse.Namespace(num_orders=3, num_warehouses=5, max_demand=500, max_inventory=200, exceed_inventory=False))

    # Edge Cases
    print("\nRunning edge cases...")
    # Minimal inputs
    generate_and_process_test_data(argparse.Namespace(num_orders=1, num_warehouses=1, max_demand=2, max_inventory=2, exceed_inventory=False)) # max_demand set to 2 here

    # Special Cases: Varying configuration
    print("\nRunning special cases...")
    for i in range(2, 12):  # From 2 to 11 warehouses with fixed orders
        generate_and_process_test_data(argparse.Namespace(num_orders=5, num_warehouses=i, max_demand=500, max_inventory=200, exceed_inventory=False))

    for i in range(2, 12):  # From 2 to 11 orders with fixed warehouses
        generate_and_process_test_data(argparse.Namespace(num_orders=i, num_warehouses=5, max_demand=500, max_inventory=200, exceed_inventory=True))

    # Extreme Demand and Inventory
    print("\nRunning extreme cases...")
    generate_and_process_test_data(argparse.Namespace(num_orders=3, num_warehouses=5, max_demand=10000, max_inventory=200, exceed_inventory=True))
    generate_and_process_test_data(argparse.Namespace(num_orders=3, num_warehouses=5, max_demand=500, max_inventory=10000, exceed_inventory=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate, process test data, and run test cases.')
    parser.add_argument('--run_tests', action='store_true', help='Flag to run multiple test cases.')
    parser.add_argument('--num_orders', type=int, default=3, help='Number of orders.')
    parser.add_argument('--num_warehouses', type=int, default=5, help='Number of warehouses.')
    parser.add_argument('--max_demand', type=int, default=500, help='Maximum demand.')
    parser.add_argument('--max_inventory', type=int, default=200, help='Maximum inventory.')
    parser.add_argument('--exceed_inventory', action='store_true', help='Flag to indicate if demand can exceed inventory.')

    args = parser.parse_args()

    if args.run_tests:
        run_test_cases()
    else:
        generate_and_process_test_data(args)
