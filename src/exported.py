



import numpy as np

def validate_inputs(X, Y, Z):
    """
    Validates the input parameters for the product allocation problem.
    
    :param X: Transport Time Matrix (2D NumPy array)
    :param Y: Demand Array (1D NumPy array)
    :param Z: Stock Array (1D NumPy array)
    :return: A boolean value indicating the validity of the inputs and a message string.
    """
    if X.ndim != 2:
        return False, "X must be a 2D array currently"
    
    if Y.ndim != 1 or Z.ndim != 1:
        return False, "Y and Z must be 1D arrays currently"
    
    rows_X, cols_X = X.shape
    if len(Y) != rows_X or len(Z) != cols_X:
        return False, "Dimensions of X, Y, and Z are not compatible"
    
    if np.any(X < 0) or np.any(Y < 0) or np.any(Z < 0):
        return False, "All elements in X, Y, and Z must be non-negative"
    
    return True, "Inputs are valid"

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

for i, case in enumerate(test_data):
    is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
    print(f"Test case {i+1} ({case['description']}): {message}")



import numpy as np

def validate_inputs(X, Y, Z):
    return True, "Valid"

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


for i, case in enumerate(test_data):
    print(f"============= Test Case {i+1} =============")
    print(f"Description: {case['description']}")
    print(f"Priority Order: {case['priority_order']}")
    print(f"Transport Time Matrix (X): \n{case['X']}")
    print(f"Demand Array (Y): {case['Y']}")
    print(f"Stock Array (Z): {case['Z']}")
    
    is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
    if is_valid:
        A, remaining_Z, remaining_Y = initial_allocation(case)
        
        print("\nInitial Allocation Matrix A:")
        print(A)
        print("Remaining Stock in Warehouses:")
        print(remaining_Z)
        print("Remaining Demand for Orders:")
        print(remaining_Y)
    else:
        print(f"\nInvalid inputs: {message}")
    print("===========================================\n")



import pulp
import numpy as np

def optimize_allocation(data):
    X = data['X']
    Y = data['Y']
    Z = data['Z']
    priority_order = data['priority_order']
    
    num_orders, num_warehouses = X.shape

    prob = pulp.LpProblem("Product_Allocation", pulp.LpMinimize)

    A_vars = pulp.LpVariable.dicts("Allocation", [(i, j) for i in range(num_orders) for j in range(num_warehouses)],
                                   0, cat='Integer')  # non-negative integers
    M = pulp.LpVariable("Max_Transport_Time", 0)  # non-negative

    prob += M, "Objective is to Minimize the Maximum Transport Time"

    for i in range(num_orders):
        for j in range(num_warehouses):
            prob += M >= X[i][j] * A_vars[(i, j)]

    for i in range(num_orders):
        prob += pulp.lpSum([A_vars[(i, j)] for j in range(num_warehouses)]) == Y[i]
        
    for j in range(num_warehouses):
        prob += pulp.lpSum([A_vars[(i, j)] for i in range(num_orders)]) <= Z[j]

    prob.solve()

    A = np.zeros((num_orders, num_warehouses))
    for i, j in A_vars:
        A[i, j] = A_vars[(i, j)].varValue

    return A



for i, case in enumerate(test_data):
    print(f"============= Test Case {i+1} =============")
    print(f"Description: {case['description']}")
    print(f"Priority Order: {case['priority_order']}")
    print(f"Transport Time Matrix (X): \n{case['X']}")
    print(f"Demand Array (Y): {case['Y']}")
    print(f"Stock Array (Z): {case['Z']}")
    
    is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
    if is_valid:
        A, remaining_Z, remaining_Y = initial_allocation(case)
        print("\nInitial Allocation Matrix A:")
        print(A)
        
        A_optimized = optimize_allocation(case)
        print("\nOptimized Allocation Matrix A:")
        print(A_optimized)
        
    else:
        print(f"\nInvalid inputs: {message}")
    print("===========================================\n")



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


for i, case in enumerate(test_data):
    print(f"============= Test Case {i+1} =============")
    print(f"Description: {case['description']}")
    print(f"Priority Order: {case['priority_order']}")
    print(f"Transport Time Matrix (X): \n{case['X']}")
    print(f"Demand Array (Y): {case['Y']}")
    print(f"Stock Array (Z): {case['Z']}")
    
    is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
    if is_valid:
        A, remaining_Z, remaining_Y = initial_allocation(case)
        print("\nInitial Allocation Matrix A:")
        print(A)
        
        A_optimized = optimize_allocation_priority(case)
        print("\nOptimized Allocation Matrix A:")
        print(A_optimized)
        
    else:
        print(f"\nInvalid inputs: {message}")
    print("===========================================\n")


def validate_allocation_priority(A, Y, Z, priority_order, expected_A=None):
    for i, y in enumerate(Y):
        if np.sum(A[:, i]) != y:
            if np.sum(A) == np.sum(Z):  # All inventory is used
                return False, f"Order {i} allocation mismatch considering priority. Expected: {y}, Got: {np.sum(A[:, i])}. But all inventory was used."
            else:
                return False, f"Order {i} allocation mismatch considering priority. Expected: {y}, Got: {np.sum(A[:, i])}."
    
    for j, z in enumerate(Z):
        if np.sum(A[j, :]) > z:
            return False, f"Warehouse {j} over allocation. Expected: <= {z}, Got: {np.sum(A[j, :])}."
    
    if np.any(A < 0):
        return False, "Negative allocation detected."
    
    if expected_A is not None:
        if not np.array_equal(A, expected_A):
            return False, "The given allocation matrix does not match the expected result."

    return True, "All constraints satisfied."


for i, case in enumerate(test_data):
    print(f"============= Test Case {i+1} =============")
    print(f"Description: {case['description']}")
    print(f"Priority Order: {case['priority_order']}")
    print(f"Transport Time Matrix (X): \n{case['X']}")
    print(f"Demand Array (Y): {case['Y']}")
    print(f"Stock Array (Z): {case['Z']}")
    
    A_optimized = optimize_allocation_priority(case)
    print("\nOptimized Allocation Matrix A:")
    print(A_optimized)
    
    is_valid, message = validate_allocation_priority(A_optimized, case['Y'], case['Z'], case['priority_order'])
    print(message)  # this will print if the allocation was valid or not
    
    print("===========================================\n")



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
    hadamard_product = np.multiply(A, X)
    
    return np.max(hadamard_product)

def main_allocation_function(case):
    """
    Optimize the product allocation and compute minimized maximum transport time.
    
    Args:
    - case (dict): Dictionary containing priority order, transport time matrix X, demand array Y, and stock array Z.
    
    Returns:
    - dict: Dictionary containing optimized allocation matrix A and minimized maximum transport time.
    """
    
    A_optimized = optimize_allocation_priority(case)
    
    max_time = compute_minimized_max_transport_time(A_optimized, case['X'])
    
    return {
        'Allocation Matrix': A_optimized,
        'Minimized Maximum Transport Time': max_time
    }

results = []
for i, case in enumerate(test_data):
    print(f"============= Test Case {i+1} =============")
    print(f"Description: {case['description']}")
    print(f"Priority Order: {case['priority_order']}")
    print(f"Transport Time Matrix (X): \n{case['X']}")
    print(f"Demand Array (Y): {case['Y']}")
    print(f"Stock Array (Z): {case['Z']}")
    
    result = main_allocation_function(case)
    
    print("\nOptimized Allocation Matrix A:")
    print(result['Allocation Matrix'])
    
    is_valid, message = validate_allocation_priority(result['Allocation Matrix'], case['Y'], case['Z'], case['priority_order'])
    print(message)  # this will print if the allocation was valid or not

    print(f"Minimized Maximum Transport Time: {result['Minimized Maximum Transport Time']}")

    print("===========================================\n")
    
    results.append(result)





small_test_data = [
    {
        'description': 'Basic case',
        'priority_order': np.array([0, 1]),
        'X': np.array([
            [1, 3],
            [2, 1]
        ]),
        'Y': np.array([5, 5]),
        'Z': np.array([10, 10]),
        'expected_A': np.array([
            [5, 0],
            [0, 5]
        ]),
        'expected_max_time': 2
    },
    {
        'description': 'Unsatisfiable Orders',
        'priority_order': np.array([0, 1]),
        'X': np.array([
            [1, 3],
            [2, 1]
        ]),
        'Y': np.array([10, 10]),
        'Z': np.array([5, 5]),
        'expected_A': np.array([
            [5, 5],
            [0, 0]
        ]),
        'expected_max_time': 3
    },
    {
        'description': 'Exact Stock',
        'priority_order': np.array([0, 1]),
        'X': np.array([
            [1, 3],
            [2, 1]
        ]),
        'Y': np.array([5, 5]),
        'Z': np.array([5, 5]),
        'expected_A': np.array([
            [5, 0],
            [0, 5]
        ]),
        'expected_max_time': 2
    },
    {
        'description': 'Varied Transport Times',
        'priority_order': np.array([0, 1]),
        'X': np.array([
            [1, 10],
            [10, 1]
        ]),
        'Y': np.array([5, 5]),
        'Z': np.array([10, 10]),
        'expected_A': np.array([
            [5, 0],
            [0, 5]
        ]),
        'expected_max_time': 10
    },
    {
        'description': 'Priorities with Insufficient Stock',
        'priority_order': np.array([1, 0]),
        'X': np.array([
            [1, 2],
            [2, 1]
        ]),
        'Y': np.array([5, 5]),
        'Z': np.array([5, 3]),
        'expected_A': np.array([
            [3, 0],
            [2, 3]
        ]),
        'expected_max_time': 3
    }
]



def test_allocation(test_data):
    results = []
    
    for i, case in enumerate(test_data):
        print(f"============= Test Case {i+1} =============")
        print(f"Description: {case['description']}")
        if 'priority_order' in case:
            print(f"Priority Order: {case['priority_order']}")
        print(f"Transport Time Matrix (X): \n{case['X']}")
        print(f"Demand Array (Y): {case['Y']}")
        print(f"Stock Array (Z): {case['Z']}")
        
        is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
        
        if is_valid:
            A, remaining_Z, remaining_Y = initial_allocation(case)
            print("\nInitial Allocation Matrix A:")
            print(A)
            
            A_optimized = optimize_allocation_priority(case)
            print("\nOptimized Allocation Matrix A:")
            print(A_optimized)
            
            is_valid, validation_message = validate_allocation_priority(A_optimized, case['Y'], case['Z'], case.get('priority_order', []))
            print(validation_message)
            
            max_transport_time = np.max(A_optimized * case['X'])
            print(f"Minimized Maximum Transport Time: {max_transport_time}")
            
            result = {
                'Allocation Matrix': A_optimized,
                'Minimized Maximum Transport Time': max_transport_time
            }
            results.append(result)
            
        else:
            print(f"\nInvalid inputs: {message}")
        
        print("===========================================\n")
    
    return results

results_small = test_allocation(small_test_data)




def generate_large_matrix(num_orders=1000, num_warehouses=1000, max_time=100):
    X = np.random.randint(1, max_time, size=(num_orders, num_warehouses))
    Y = np.random.randint(10, 100, size=num_orders)
    Z = np.random.randint(10, 100, size=num_warehouses)
    priority_order = np.arange(num_orders)
    np.random.shuffle(priority_order)
    return {
        'description': 'Large Number of Orders and Warehouses',
        'X': X,
        'Y': Y,
        'Z': Z,
        'priority_order': priority_order
    }

def generate_high_demand_and_inventory(num_orders=100, num_warehouses=100, max_demand=10000, max_inventory=10000):
    X = np.random.randint(1, 100, size=(num_orders, num_warehouses))
    Y = np.random.randint(1, max_demand, size=num_orders)
    Z = np.random.randint(1, max_inventory, size=num_warehouses)
    priority_order = np.arange(num_orders)
    np.random.shuffle(priority_order)
    return {
        'description': 'High Demand and Inventory',
        'X': X,
        'Y': Y,
        'Z': Z,
        'priority_order': priority_order
    }

def generate_combination(num_orders=500, num_warehouses=500, max_time=100, max_demand=5000, max_inventory=5000):
    X = np.random.randint(1, max_time, size=(num_orders, num_warehouses))
    Y = np.random.randint(1, max_demand, size=num_orders)
    Z = np.random.randint(1, max_inventory, size=num_warehouses)
    priority_order = np.arange(num_orders)
    np.random.shuffle(priority_order)
    return {
        'description': 'Combination of Both',
        'X': X,
        'Y': Y,
        'Z': Z,
        'priority_order': priority_order
    }

large_test_data = [
    generate_large_matrix(250,250),
    generate_high_demand_and_inventory(500,500),
    generate_combination(500,500)
]


results_large = test_allocation(large_test_data)




