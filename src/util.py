import numpy as np
import json

import numpy as np
import json

def json_to_matrices(json_data):
    m = len(json_data['spdd'])  # number of orders

    # Create a dictionary to map goods to units
    goods_dict = {}
    for warehouse in json_data['ck']:
        warehouse_id = list(warehouse.keys())[0]
        for good in warehouse[warehouse_id]:
            if good['spnm'] not in goods_dict:
                goods_dict[good['spnm']] = good['lg']
    
    # Create a list of warehouses based on their order in 'ckdata'
    all_warehouses = [data['cknm'] for order in json_data['spdd'] for data in order['ckdata']]

    all_goods_spdd = [order['spnm'] for order in json_data['spdd']]
    all_goods_ck = list(goods_dict.keys())
    all_goods = sorted(list(set(all_goods_spdd + all_goods_ck)))
    k = len(all_goods)  # Number of unique goods
    n = len(all_warehouses)  # number of warehouses
    
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
    
    for i, warehouse_id in enumerate(all_warehouses):
        for warehouse in json_data['ck']:
            if warehouse_id == list(warehouse.keys())[0]:
                for good in warehouse[warehouse_id]:
                    good_id = all_goods.index(good['spnm'])
                    A3[i, good_id] = good['sl']

    order_list = json_data['spdd']
    warehouse_list = all_warehouses
    goods_list = all_goods
    
    return A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list, goods_dict

if __name__=='__main__':
    with open('data.json', 'r') as f:
        json_data = json.load(f)
    A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list, goods_dict = json_to_matrices(json_data)
    print(order_list)
    print(warehouse_list)
    print(goods_list)
    print(goods_dict)
