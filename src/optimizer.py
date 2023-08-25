import numpy as np

def calculate_transportation_time(A, X):
    return A * X

def brute_force_optimal_allocation(X, Y, Z, priority_order):
    m, n = len(Y), len(Z)
    optimal_A = np.zeros((m, n))
    optimal_time = float('inf')
    
    def explore_allocation(order_index, current_A, remaining_inventory):
        nonlocal optimal_A, optimal_time
        
        if order_index == m:
            B = calculate_transportation_time(current_A, X)
            max_time = B.max()
            if max_time < optimal_time:
                optimal_A = current_A.copy()
                optimal_time = max_time
            return

        order_priority = priority_order[order_index]
        
        for j in range(n):
            allocation = min(Y[order_priority] - sum(current_A[order_priority, :]), remaining_inventory[j])
            current_A[order_priority, j] = allocation
            new_remaining_inventory = remaining_inventory.copy()
            new_remaining_inventory[j] -= allocation
            explore_allocation(order_index + 1, current_A.copy(), new_remaining_inventory)

    explore_allocation(0, np.zeros((m, n)), Z)
    return optimal_A, optimal_time
