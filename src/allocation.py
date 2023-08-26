import numpy as np

def brute_force_allocation(X, Y, Z, priority_order):
    """
    X: Transportation time matrix (order x warehouse)
    Y: Demand matrix (order x 1)
    Z: Inventory matrix (warehouse x 1)
    priority_order: Priority list of orders
    
    Returns:
    A: Allocation matrix (order x warehouse)
    max_time: The maximum transportation time
    """
    
    m, n = X.shape  # m is number of orders, n is number of warehouses
    
    # Initialize allocation matrix with zeros
    A = np.zeros((m, n))
    
    # List to store all possible allocation combinations
    all_allocations = []
    
    # Iterate over each order based on priority
    for order_index in priority_order:
        remaining_inventory = Z.copy()
        for j in range(n):
            # Calculate the allocation for the order and warehouse
            allocation = min(Y[order_index], remaining_inventory[j])
            
            # Update the allocation matrix
            A[order_index][j] = allocation
            
            # Update the remaining demand and inventory
            Y[order_index] -= allocation
            remaining_inventory[j] -= allocation
            
            # If the order demand is satisfied, break out of the loop
            if Y[order_index] == 0:
                break
        
        # Store the current allocation matrix in the list of all possible allocations
        all_allocations.append(A.copy())
    
    # Calculate the transportation time for each allocation matrix and select the one with the minimum max time
    min_max_time = float('inf')
    best_allocation = None
    for allocation in all_allocations:
        transport_time = allocation * X
        max_time = np.max(transport_time)
        if max_time < min_max_time:
            min_max_time = max_time
            best_allocation = allocation
    
    return best_allocation, min_max_time
