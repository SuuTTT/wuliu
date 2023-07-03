import numpy as np
import json

import numpy as np
import json

def json_to_matrices(json_data):
    m = len(json_data['spdd'])  # number of orders
    n = len(json_data['ck'])  # number of warehouses
    # Determine the number of goods
    all_goods_spdd = [order['spnm'] for order in json_data['spdd']]
    all_goods_ck = [good['spnm'] for warehouse in json_data['ck'] for good in warehouse[list(warehouse.keys())[0]]]
    all_goods = sorted(list(set(all_goods_spdd + all_goods_ck)))
    k = len(all_goods)  # Number of unique goods

    # Initialize matrices
    A1 = np.zeros((m, n, k))
    A2 = np.zeros((m, k))
    A3 = np.zeros((n, k))
    W1 = 1 / np.arange(1, m+1)  # We consider the priority of orders to be inversely proportional to their order
    W2 = 1 / np.arange(1, n+1)  # We consider the priority of warehouses to be inversely proportional to their order

    for i, order in enumerate(json_data['spdd']):
        good_id = all_goods.index(order['spnm'])
        A2[i, good_id] = order['sl']
        for j, ckdata in enumerate(order['ckdata']):
            A1[i, j, good_id] = ckdata['dwyssj']

    for i, warehouse in enumerate(json_data['ck']):
        for j, good in enumerate(warehouse[list(warehouse.keys())[0]]):
            good_id = all_goods.index(good['spnm'])
            A3[i, good_id] = good['sl']

    return A1, A2, A3, W1, W2