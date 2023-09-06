import numpy as np

from itertools import product

import json
from scipy.optimize import linprog

def lp_allocation(X, Y, Z, T):
    m, n = X.shape
    
    # Flatten the X matrix to a 1D array
    c = np.zeros(m * n)
    
    # Inequality constraints: for each order, the sum of allocations should be >= demand
    A_ineq = np.zeros((m, m * n))
    for i in range(m):
        A_ineq[i, i * n:(i + 1) * n] = -1
    b_ineq = -Y

    # Equality constraints: for each warehouse, the sum of allocations should be <= inventory
    A_eq = np.zeros((n, m * n))
    for j in range(n):
        A_eq[j, j::n] = 1
    b_eq = Z
    
    # Additional constraint: for each pair (i, j), a_ij * X_ij <= T
    A_T = np.zeros((m * n, m * n))
    np.fill_diagonal(A_T, X.flatten())
    b_T = np.full(m * n, T)
    
    # Concatenate all constraints
    A_ineq = np.concatenate([A_ineq, A_T], axis=0)
    b_ineq = np.concatenate([b_ineq, b_T])
    
    # Bounds for each variable (0 <= a_ij <= 1)
    x_bounds = (0, 1)
    bounds = [x_bounds] * (m * n)
    
    # Solve the linear program
    result = linprog(c, A_ub=A_ineq, b_ub=b_ineq, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    if result.success:
        # Extract the allocation matrix from the result
        allocation_matrix = np.array(result.x).reshape((m, n))
        return allocation_matrix, True
    else:
        return None, False

def binary_search_allocation(X, Y, Z):
    low_T = 0
    high_T = np.max(X) * np.max(Y)
    tolerance = 1e-5
    optimal_allocation = None
    
    while high_T - low_T > tolerance:
        mid_T = (high_T + low_T) / 2.0
        allocation_matrix, is_feasible = lp_allocation(X, Y, Z, mid_T)
        
        if is_feasible:
            high_T = mid_T
            optimal_allocation = allocation_matrix
        else:
            low_T = mid_T
            
    optimal_T = (high_T + low_T) / 2.0
    return optimal_allocation, optimal_T

def brute_force_optimal_allocation(X, Y, Z, priority_order):
    m, n = Y.shape[0], Z.shape[0]
    
    # Check if the total demand is less than or equal to the total inventory
    if np.sum(Y) <= np.sum(Z):
        # In this case, we can fully satisfy all orders
        # We'll use the binary search approach to find the optimal allocation
        allocation_matrix, optimal_T = binary_search_allocation(X, Y, Z)
        return allocation_matrix, optimal_T
    
    # If the total demand exceeds the total inventory
    else:
        # Identify up to which priority order the demands can be fully met
        total_inventory = np.sum(Z)
        last_fully_satisfied_order_index = -1
        for i in priority_order:
            if Y[i] <= total_inventory:
                last_fully_satisfied_order_index = i
                total_inventory -= Y[i]
            else:
                break
        
        # Only consider the orders up to the last order that can be fully satisfied
        # and allocate the remaining inventory to the next order in priority
        if last_fully_satisfied_order_index != -1:
            new_Y = Y[:last_fully_satisfied_order_index+1].copy()
            if last_fully_satisfied_order_index+1 < m:
                new_Y = np.append(new_Y, total_inventory)
            new_priority_order = priority_order[:last_fully_satisfied_order_index+2]
        else:
            new_Y = np.array([total_inventory])
            new_priority_order = np.array([priority_order[0]])
        
        allocation_matrix, optimal_T = binary_search_allocation(X[:len(new_Y)], new_Y, Z)
        return allocation_matrix, optimal_T

# Don't forget to include the 'lp_allocation' and 'binary_search_allocation' functions from the previous code snippet.


if __name__=='__main__':


    # Test data definitions
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
            'X': np.array([[1, 4], [4, 2]]),
            'Y': np.array([1, 1]),
            'Z': np.array([3, 4]),
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

    # Test execution
    test_results = []
    for i, test_case in enumerate(test_data):
        X, Y, Z, priority_order, description = test_case.values()
        allocation_matrix, max_transport_time = brute_force_optimal_allocation(X, Y, Z, priority_order)
        test_results.append({
            'test_case': i + 1,
            'description': description,
            'allocation_matrix': allocation_matrix.tolist(),
            'max_transport_time': max_transport_time
        })

    print(json.dumps(test_results, indent=2))
