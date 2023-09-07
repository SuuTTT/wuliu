import numpy as np
import pulp
import numpy as np


def initial_allocation(data):
    """
    Perform initial allocation based on the minimum transport times.

    :param data: A dictionary containing X, Y, and Z
    :return: Initial Allocation Matrix A, Remaining Stock, Remaining Demand
    """
    X = data['X']
    Y = data['Y']
    Z = data['Z']

    A = np.zeros_like(X)
    remaining_Y = np.copy(Y)
    remaining_Z = np.copy(Z)

    sorted_idx = np.unravel_index(np.argsort(X, axis=None), X.shape)
    for i, j in zip(*sorted_idx):
        if remaining_Y[i] == 0 or remaining_Z[j] == 0:
            continue
        allocate_amount = min(remaining_Y[i], remaining_Z[j])
        A[i, j] += allocate_amount
        remaining_Y[i] -= allocate_amount
        remaining_Z[j] -= allocate_amount

    return A, remaining_Z, remaining_Y


def optimize_allocation(data):
    X = data['X']
    Y = data['Y']
    Z = data['Z']
    priority_order = data['priority_order']
    
    num_orders, num_warehouses = X.shape

    # Initialize the ILP problem
    prob = pulp.LpProblem("Product_Allocation", pulp.LpMinimize)

    # Decision Variables (integer type specified)
    A_vars = pulp.LpVariable.dicts("Allocation", [(i, j) for i in range(num_orders) for j in range(num_warehouses)],
                                   0, cat='Integer')  # non-negative integers
    M = pulp.LpVariable("Max_Transport_Time", 0)  # non-negative

    # Objective Function
    prob += M, "Objective is to Minimize the Maximum Transport Time"

    # Constraints
    # Set M to be greater than every element in the Hadamard product of X and A
    for i in range(num_orders):
        for j in range(num_warehouses):
            prob += M >= X[i][j] * A_vars[(i, j)]

    # Adjusted Constraint: Ensure sum of allocations for each order is exactly the demand
    for i in range(num_orders):
        prob += pulp.lpSum([A_vars[(i, j)] for j in range(num_warehouses)]) == Y[i]
        
    # Ensure sum of allocations for each warehouse is <= inventory
    for j in range(num_warehouses):
        prob += pulp.lpSum([A_vars[(i, j)] for i in range(num_orders)]) <= Z[j]

    # Solve
    prob.solve()


    # Extract values of A_vars into a matrix form
    A = np.zeros((num_orders, num_warehouses))
    for i, j in A_vars:
        A[i, j] = A_vars[(i, j)].varValue

    return A


def allocate_based_on_priority(Y, Z, priority_order):
    A = np.zeros((len(Y), len(Z)))
    for order_index in priority_order:
        for warehouse_index in range(len(Z)):
            allocation = min(Z[warehouse_index], Y[order_index])
            A[order_index][warehouse_index] = allocation
            Z[warehouse_index] -= allocation
            Y[order_index] -= allocation
    return A

def optimize_allocation_priority(data):
    X = data['X']
    Y = data['Y'].copy()  # We make a copy since we modify it
    Z = data['Z'].copy()  # We make a copy since we modify it
    priority_order = data['priority_order']
    
    A, remaining_Z, remaining_Y = initial_allocation(data)
    
    if np.sum(remaining_Y) > 0:  # Not all orders can be satisfied
        A = allocate_based_on_priority(Y, Z, priority_order)
    else:  # All orders can be satisfied
        A = optimize_allocation(data)
    
    return A

def validate_allocation_priority(A, Y, Z, priority_order, expected_A=None):
    # Validate if sum of allocations for each order i is equal to Yi
    for i, y in enumerate(Y):
        if np.sum(A[:, i]) != y:
            if np.sum(A) == np.sum(Z):  # All inventory is used
                return False, f"Order {i} allocation mismatch considering priority. Expected: {y}, Got: {np.sum(A[:, i])}. But all inventory was used."
            else:
                return False, f"Order {i} allocation mismatch considering priority. Expected: {y}, Got: {np.sum(A[:, i])}."
    
    # Validate if sum of allocations from each warehouse j does not exceed Zj
    for j, z in enumerate(Z):
        if np.sum(A[j, :]) > z:
            return False, f"Warehouse {j} over allocation. Expected: <= {z}, Got: {np.sum(A[j, :])}."
    
    # Validate if all elements in A are greater than or equal to 0
    if np.any(A < 0):
        return False, "Negative allocation detected."
    
    # If expected_A is provided, compare with the given A
    if expected_A is not None:
        if not np.array_equal(A, expected_A):
            return False, "The given allocation matrix does not match the expected result."

    return True, "All constraints satisfied."


import numpy as np

def compute_minimized_max_transport_time(A, X):
    """
    Compute the minimized maximum transport time based on allocation matrix A and transport time matrix X.
    
    Args:
    - A (numpy.ndarray): Allocation matrix.
    - X (numpy.ndarray): Transport time matrix.
    
    Returns:
    - float: Minimized maximum transport time.
    """
    # Compute the Hadamard product
    hadamard_product = np.multiply(A, X)
    
    # Find and return the maximum value in the matrix
    return np.max(hadamard_product)

def main_allocation_function(case):
    """
    Optimize the product allocation and compute minimized maximum transport time.
    
    Args:
    - case (dict): Dictionary containing priority order, transport time matrix X, demand array Y, and stock array Z.
    
    Returns:
    - dict: Dictionary containing optimized allocation matrix A and minimized maximum transport time.
    """
    
    # Optimize allocation considering priority
    A_optimized = optimize_allocation_priority(case)
    
    # Compute minimized maximum transport time
    max_time = compute_minimized_max_transport_time(A_optimized, case['X'])
    
    return {
        'Allocation Matrix': A_optimized,
        'Minimized Maximum Transport Time': max_time
    }


def main():
    # Assuming you have defined test_data somewhere before this, or it could be imported
    test_data = [
        {
            'X': np.array([[4, 2], [3, 2]]),
            'Y': np.array([1, 1]),
            'Z': np.array([3, 4]),
            'priority_order': np.array([0, 1]),
            'description': "All orders can be satisfied, no priority needed"
        },
        {
            'X': np.array([[2, 8], [1, 4]]),
            'Y': np.array([10, 5]),
            'Z': np.array([5, 5]),
            'priority_order': np.array([0, 1]),
            'description': "Not all orders can be satisfied, and priority comes into play"
        },
        {
            'X': np.array([[1, 1], [1, 2]]),
            'Y': np.array([1, 1]),
            'Z': np.array([1, 1]),
            'priority_order': np.array([0, 1]),
            'description': "All orders can be satisfied, but not in a greedy manner"
        },
        {
            'X': np.array([[1], [0], [2]]),
            'Y': np.array([1, 1, 2]),
            'Z': np.array([2]),
            'priority_order': np.array([2, 1, 0]),
            'description': "Not all orders can be satisfied, and priority comes into play"
        },
        {
            'X': np.array([[1]]),
            'Y': np.array([1]),
            'Z': np.array([1]),
            'priority_order': np.array([0]),
            'description': "All orders can be satisfied, no priority needed"
        },
        {
            'X': np.array([[1, 1], [0, 0]]),
            'Y': np.array([1, 1]),
            'Z': np.array([1, 1]),
            'priority_order': np.array([1, 0]),
            'description': "Not all orders can be satisfied, but all warehouses can contribute to the high priority order"
        },
        {
            'X': np.array([[1., 4.],
                        [2., 2.],
                        [4., 2.],
                        [2., 1.],
                        [1., 4.]]), 
            'Y': np.array([46., 26.,  6., 27., 17.]),
            'Z': np.array([2., 18.]),
            'priority_order': np.array([3, 4, 1, 0, 2]),
            'description': "Complex case"
        }
    ]
    from util import append_data
    # Example of appending generated data
    test_data = append_data(test_data, source='generated', num_orders=5, num_warehouses=3, max_demand=10, max_inventory=7, description="Generated data example")

    # Example of appending data from a file
    test_data = append_data(test_data, source='file', filename="tmp/test_data.json", description="Data loaded from file")

    results = []
    for i, case in enumerate(test_data):
        print(f"============= Test Case {i+1} =============")
        print(f"Description: {case['description']}")
        print(f"Priority Order: {case['priority_order']}")
        print(f"Transport Time Matrix (X): \n{case['X']}")
        print(f"Demand Array (Y): {case['Y']}")
        print(f"Stock Array (Z): {case['Z']}")
        
        # Get the results from the main function
        result = main_allocation_function(case)
        
        print("\nOptimized Allocation Matrix A:")
        print(result['Allocation Matrix'])
        
        is_valid, message = validate_allocation_priority(result['Allocation Matrix'], case['Y'], case['Z'], case['priority_order'])
        print(message)  # this will print if the allocation was valid or not

        print(f"Minimized Maximum Transport Time: {result['Minimized Maximum Transport Time']}")
        print("===========================================\n")
        
        results.append(result)

if __name__ == "__main__":
    main()