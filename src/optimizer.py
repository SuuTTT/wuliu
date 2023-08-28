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


def iterative_allocation(X, Y, Z):
    m, n = X.shape
    allocation = np.zeros((m, n))
    remaining_demand = Y.copy()
    remaining_supply = Z.copy()
    
    # Sorting orders based on their priority
    order_priority = np.argsort(np.sum(X, axis=1))
    
    for i in order_priority:
        for j in np.argsort(X[i]):
            # Allocate as much as possible from the current warehouse to the current order
            allocation_amount = min(remaining_supply[j], remaining_demand[i])
            allocation[i, j] = allocation_amount
            remaining_supply[j] -= allocation_amount
            remaining_demand[i] -= allocation_amount

    return allocation

import numpy as np
from scipy.optimize import linprog

def linear_programming_allocation(X, Y, Z, priority_order):
    m, n = X.shape  # m is number of orders, n is number of warehouses
    
    # Decision Variables: a_ij for each order i and warehouse j, and an additional M
    num_vars = m * n + 1

    # Coefficients for the objective function
    c = [0] * (m * n) + [1]  # Only the M variable has a coefficient in the objective
    
    # Constraints
    A_eq = []  # Coefficient matrix for equality constraints
    b_eq = []  # RHS values for equality constraints

    A_ub = []  # Coefficient matrix for inequality constraints
    b_ub = []  # RHS values for inequality constraints
    
    # Demand constraints
    for i in range(m):
        A_row = [0] * num_vars
        for j in range(n):
            A_row[i*n + j] = 1
        A_ub.append(A_row)
        b_ub.append(Y[i])
    
    # Inventory constraints
    for j in range(n):
        A_row = [0] * num_vars
        for i in range(m):
            A_row[i*n + j] = 1
        A_ub.append(A_row)
        b_ub.append(Z[j])
    
    # Transportation time constraints
    for i in range(m):
        for j in range(n):
            A_row = [0] * num_vars
            A_row[i*n + j] = X[i, j]
            A_row[-1] = -1  # Coefficient for M
            A_ub.append(A_row)
            b_ub.append(0)

    # Bounds for the decision variables
    x_bounds = [(0, None) for _ in range(num_vars)]
    x_bounds[-1] = (0, np.max(X)*np.max(Y))  # Bounds for M based on maximum possible transportation time
    
    # Solve the linear program
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='simplex')
    
    # Extract allocation matrix and max transport time from the result
    allocation = np.array(result.x[:-1]).reshape(m, n)
    max_time = result.x[-1]

    return allocation, max_time

if __name__=='__main__':
    # Define the data matrices again
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    Y = np.array([10, 15, 20])
    Z = np.array([25, 25, 25])
    priority_order = [2, 0, 1]

    # Re-run the LP-based allocation method with the provided data
    lp_allocation, lp_max_transport = linear_programming_allocation(X, Y, Z, priority_order)
    lp_allocation, lp_max_transport

