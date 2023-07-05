import numpy as np
import json
from util import json_to_matrices
from optimizer import logistics_distribution
def test_function():
    with open("data/data_5.txt") as f:
        json_data = json.load(f)

    A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list,goods_dict = json_to_matrices(json_data)

    for i in range(A1.shape[0]):
        for j in range(A1.shape[1]):
            print(f"For order {i+1}, warehouse {j+1}, the unit transportation times are {A1[i, j]} for goods {list(range(1, A1.shape[2]+1))}")
    
    print("A2: Demand for each type of good for each order. Each row corresponds to an order, each column corresponds to a good.")
    print(A2)

    print("A3: Stock of each type of good in each warehouse. Each row corresponds to a warehouse, each column corresponds to a good.")
    print(A3)

    print("W1: Priority of each order. The lower the index, the higher the priority.")
    print(W1)

    print("W2: Priority of each warehouse. The lower the index, the higher the priority.")
    print(W2)
    result = logistics_distribution(A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list,goods_dict)
    #logistics_distribution(A1, A2, A3, W1, W2)
    print(result)
    
if __name__ == "__main__":
    test_function()