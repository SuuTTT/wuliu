# README

## intro

this branch use the naive brute force method to solve the problem. mainly used to 

1. generate the test data
2. verify the correctness of the algorithm (comparison test)
3. clarify the problem and requirements


## usage

```bash
# generate the test data
python3 generate_test_data.py

# run the test
python3 test.py
```

## tutorial

### key concept

**Allocation Combination:**
An allocation combination represents one possible way to distribute goods from warehouses to a specific order. It is a tuple that contains the amount of goods allocated from each warehouse to fulfill the demand for the order. For example, if we have 2 warehouses and need to fulfill an order of 10 units, an allocation combination might be (4, 6), meaning 4 units from warehouse 1 and 6 units from warehouse 2.

**Remaining Inventory:**
Remaining inventory is a vector that keeps track of how many goods are left in each warehouse after the allocation for the current order. As we allocate goods from the warehouses to fulfill an order, we reduce the remaining inventory accordingly. This ensures that we don't allocate more goods than are available in the warehouses.

### coding trick

Use of product:
The product function from the itertools module is used to generate all possible combinations of allocations for the current order. By using the product function with the allocation ranges for each warehouse, we can explore every possible way to fulfill the order's demand from the available inventory in the warehouses. This is essential for the brute-force method, as we want to examine all possible allocations to find the optimal one.

