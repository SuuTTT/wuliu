# README

## intro

this branch use the naive method(greedy, brute force, linear programming) to solve the problem. 
mainly used to 
1. clarify the problem and requirements
2. generate the test data
3. verify the correctness of the algorithm (comparison test)



## usage

```bash
# generate the test data
python generate_test_data.py --run_tests

# run the test
python3 test.py
```

## tutorial




### problem definition
Below, we formalize the problem with  with a example where greedy algorithm fails to find the optimal solution:

Given the transportation times(row is order, column is warehouse):

\[
X = \begin{pmatrix}
2 & 8 \\
1 & 4
\end{pmatrix}
\]

 **Greedy Algorithm**:

1. **For \( O_1 \)** (Highest Priority Order):
   - Transportation time from \( W_1 \) to \( O_1 \) is 2 hours.
   - Transportation time from \( W_2 \) to \( O_1 \) is 8 hours.
   - Greedy choice: Allocate from \( W_1 \) to \( O_1 \) since 2 < 8.

2. **For \( O_2 \)** (Next Priority Order):
   - \( W_1 \) has already been allocated, so the only available option is \( W_2 \).
   - Allocate from \( W_2 \) to \( O_2 \).

Resulting Allocation:
\[
A_{\text{greedy}} = \begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}
\]
Maximum transportation time: 8 hours (from \( W_2 \) to \( O_1 \)).

 **Optimal Allocation**:

1. **For \( O_1 \)**:
   - Despite the longer transportation time from \( W_2 \), allocate from \( W_2 \) to \( O_1 \).

2. **For \( O_2 \)**:
   - Allocate from \( W_1 \) to \( O_2 \).

Resulting Allocation:
\[
A_{\text{optimal}} = \begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}
\]
Maximum transportation time: 4 hours (from \( W_2 \) to \( O_2 \)).
 the greedy algorithm fails to find the optimal solution because it doesn't foresee that allocating from \( W_1 \) to \( O_1 \) would result in a longer maximum transportation time for \( O_2 \).

next, we will specify our additional requirements for some special cases.

### additional requirements

#### 1. Exceeding Inventory

in this case, we should ensure the order of higher priority is satisfied first.

\[
X = \begin{pmatrix}
2 & 8 \\
1 & 4
\end{pmatrix}
\]

Where:
- \(O_1\) requires 10 units and is the top priority order.
- \(O_2\) also requires 10 units.
- There are two warehouses, \(W_1\) and \(W_2\), with 5 units each.

** Desired Behavior**
For the order \(O_1\), we would ideally want to allocate 5 units from each warehouse, resulting in a maximum transportation time of max\((2*5,5*8)=40\) hours. Then, for \(O_2\), we would have no remaining inventory, so no allocation is made. This would result in a matrix:
\[
A = \begin{pmatrix}
5 & 5 \\
0 & 0
\end{pmatrix}
\]

#### review
is the additional requirement consistent with the original requirement? I doubt that there may be some conflict between the two requirements. making it's impossible to find a solution that satisfies both requirements.



### key concept

**Allocation Combination:**
An allocation combination represents one possible way to distribute goods from warehouses to a specific order. It is a tuple that contains the amount of goods allocated from each warehouse to fulfill the demand for the order. For example, if we have 2 warehouses and need to fulfill an order of 10 units, an allocation combination might be (4, 6), meaning 4 units from warehouse 1 and 6 units from warehouse 2.

**Remaining Inventory:**
Remaining inventory is a vector that keeps track of how many goods are left in each warehouse after the allocation for the current order. As we allocate goods from the warehouses to fulfill an order, we reduce the remaining inventory accordingly. This ensures that we don't allocate more goods than are available in the warehouses.

### coding trick

Use  product in itertools to generate all possible allocation combinations:
The product function from the itertools module is used to generate all possible combinations of allocations for the current order. By using the product function with the allocation ranges for each warehouse, we can explore every possible way to fulfill the order's demand from the available inventory in the warehouses. This is essential for the brute-force method, as we want to examine all possible allocations to find the optimal one.



## algorithm design
###  More About Optimal Goods Allocation Algorithms

his document introduces algorithms designed to optimally allocate goods from multiple warehouses to various orders. Both methods aim to minimize the maximum transportation time while respecting the inventory constraints of the warehouses and the demand of the orders.

#### 1. Brute Force Allocation (`brute_force_optimal_allocation`)

This method exhaustively explores all possible allocation combinations, making it capable of finding the globally optimal solution.

##### Key Features:
- **Exhaustive Search**: Explores every possible way to distribute goods from warehouses to orders.
- **Global Optimization**: Finds the globally optimal solution due to its exhaustive nature.
- **Order Prioritization**: Respects the given priority order of orders during the exploration.

##### Time Complexity:
Due to its exhaustive nature, this method can be computationally expensive and time-consuming, especially for a larger number of orders and warehouses.

#### 2. Iterative Allocation (`iterative_allocation`)

This method uses an iterative and greedy approach to allocate goods based on transportation times and order priority.

##### Key Features:
- **Greedy Allocation**: Makes allocation decisions iteratively based on current circumstances, favoring shorter transportation times.
- **Local Optimization**: Might not always find the globally optimal solution but is often close to optimal and much faster.
- **Order Prioritization**: Allocates goods to higher-priority orders first, ensuring that orders with higher importance are satisfied first.

##### Time Complexity:
The iterative method is more suitable for larger problem instances due to its lower time complexity.



#### 3. linear programming
our objective is to minimize \( M \), the maximum transportation time across all warehouse-to-order pairs.

Here's how we approach this:

1. **Define the Decision Variables**:
   - \( a_{ij} \): Represents the quantity of goods sent from warehouse \( j \) to order \( i \).
   - \( M \): Represents the maximum transportation time across all warehouse-to-order pairs. This is what we aim to minimize.

2. **Objective Function**:
\[
\text{Minimize } M
\]

1. **Constraints**:
   - **Demand Constraints**: Ensure that the total allocation for each order from all warehouses doesn't exceed its demand.
\[
\sum_{j=1}^{n} a_{ij} \leq Y_i \quad \text{for all } i
\]
   - **Supply Constraints**: Ensure that the total allocation from each warehouse to all orders doesn't exceed its inventory.
\[
\sum_{i=1}^{m} a_{ij} \leq Z_j \quad \text{for all } j
\]
   - **Transportation Time Constraints**: Ensure that the transportation time for each warehouse-to-order pair does not exceed \( M \).
\[
a_{ij} \times X_{ij} \leq M \quad \text{for all } i, j
\]

1. **Solution**:
   - We provide this objective function and constraints to a linear programming solver. The solver will then find values for the decision variables \( a_{ij} \) and \( M \) that minimize \( M \) while satisfying all the constraints.
   - The optimal solution will give us the allocation that ensures the worst-case transportation time (maximum transportation time across all pairs) is as low as possible.

In essence, the LP solver finds a way to allocate goods such that no single order-warehouse pair has a transportation time exceeding \( M \), and our goal is to keep \( M \) as small as possible. By minimizing \( M \), we are ensuring that the worst-case transportation time is minimized.

## More about Test

### Running Tests for Allocation System

#### Quick Start:

1. **Run predefined test scenarios**:
```bash
python generate_test_data.py --run_tests
```

2. **Custom test configuration**:
```bash
python generate_test_data.py --num_orders [NUMBER] --num_warehouses [NUMBER] --max_demand [NUMBER] --max_inventory [NUMBER] [--exceed_inventory]
```
Replace `[NUMBER]` with desired values. Use `--exceed_inventory` if the demand can exceed inventory.

### Test Configurations:

- **Baseline Test**: The standard setup for regular testing.

- **Edge Cases**:
    * **Minimal Inputs**: The smallest possible inputs to test system behavior.

- **Special Scenarios**:
    * **Varying Warehouses**: Constant order number; variable warehouses.
    * **Varying Orders**: Constant warehouse number; variable orders.

- **Extreme Tests**:
    * **High Demand**: Exaggerated demand values.
    * **High Inventory**: Exaggerated inventory values.

For each scenario, datasets are created, processed with the allocation algorithm, and saved in the `data_gen` directory. The results, such as the allocation matrix and max transport time, are also displayed.

### Test case design

