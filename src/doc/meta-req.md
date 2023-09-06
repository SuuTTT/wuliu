

**Meta-Requirement Specification for Algorithm Generation:**

**1. What would you like ChatGPT to know about you to provide better responses? (Contextual Information)**

- **Problem Context**: The project's goal is to develop a product allocation algorithm. specifically, allocating one type of product from multiple warehouses to multiple orders.  The input to this algorithm consists of the transport time matrix X between warehouses and orders (per unit), an array Y specifying the demand of each order, and an array Z detailing the current stock of the product in each warehouse. The output should be a matrix A indicating the volume of product transported from each warehouse to each order, and the minimize the maximum transportation time, i.e. elements in  Hadamard product fo A and X.
- **Technical Environment**: operate within a modified Jupyter Notebook environment.Python Version: 3.8.10
Operating System: Linux.access to a virtual drive at /mnt/data. can't access the internet in real-time.
- **Known Constraints**: Sum of allocations for each order≥Demand, Sum of allocations for each warehouse≤Inventory; the objective is to minimize the maximum transportation time across all warehouse-order allocation pairs.
- **Prior Attempts or Solutions**: due to context length limitations, I can't provide it.

**2. How would you like ChatGPT to respond? (Formatting and Structure)**

- **Algorithm Format**: if i ask for code, give direct runnable python with comments help me understand the code.
- **Step-wise Explanation**: if i ask for explaination, accompany the algorithm by a step-by-step explanation.
- **Complexity Analysis**: if i ask, give  the time and space complexity would be beneficial to ensure that the solution is efficient.
- **Use Cases**: if i ask for test, gen sample use cases or scenarios where the algorithm would be applicable and test with it

---

**Prompting Process for Algorithm Implementation:**

**Step 1**: Start with the high-level problem.
- **Prompt**: "I need an algorithm to sort a dataset of patient records based on age."

**Step 2**: Provide any known constraints or specifics.
- **Prompt**: "The solution should run in O(n log n) time complexity, and I intend to implement it in Python 3.8."

**Step 3**: Ask for the desired format or breakdown.
- **Prompt**: "Can you provide a step-by-step explanation of how this algorithm would work, followed by a pseudocode representation?"

**Step 4**: Once you have the pseudocode or the high-level approach, you can delve into the coding phase.
- **Prompt**: "Now, based on the provided pseudocode, can you generate Python code that implements this algorithm?"

**Step 5**: After obtaining the code, request additional details or refinements.
- **Prompt**: "Could you provide an analysis of the algorithm's time and space complexity? Also, offer some test cases to validate its correctness."

---

By approaching GPT-4 or similar models in this segmented and iterative manner, you can ensure clarity at each step and make any necessary refinements before proceeding to the next phase.