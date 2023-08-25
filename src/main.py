from util import *
from optimizer import brute_force_optimal_allocation

# Step 1: Generate test data in the JSON format
filename = "test_data.json"
test_data, X, Y, Z, priority_order = generate_test_data_json(3, 5, 500, 200, exceed_inventory=True)

# Step 2: Save the test data to a file
save_test_data(filename, test_data)

# Step 3: Load the test data from the file
loaded_data = load_test_data(filename)

# Convert the loaded JSON data to matrices
A1, A2, A3, priority_order, order_list, warehouse_list, goods_dict = json_to_matrices(loaded_data)

# Step 4: Compute the correct result using the brute force method
allocation_matrix, max_transport_time = brute_force_optimal_allocation(A1, A2, A3, priority_order)

# Display the allocation matrix and max transport time
print("Allocation Matrix:\n", allocation_matrix)
print("\nMax Transport Time:", max_transport_time)

# Step 5: Save the result
# Step 5: Save the result
result_filename = "test_result.txt"
with open(result_filename, 'w') as f:
    f.write("Allocation Matrix:\n")
    for row in allocation_matrix:
        f.write(" ".join(map(str, row)) + "\n")
    f.write("\nMax Transport Time: " + str(max_transport_time))

with open(filename, 'r') as f:
    saved_data = json.load(f)

saved_data