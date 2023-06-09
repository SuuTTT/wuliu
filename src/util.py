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
    
    # Removing duplicates while preserving the order
    all_warehouses = list(dict.fromkeys(all_warehouses))

    all_goods_spdd = [order['spnm'] for order in json_data['spdd']]
    all_goods_ck = list(goods_dict.keys())
    all_goods = sorted(list(set(all_goods_spdd + all_goods_ck)))
    k = len(all_goods)  # Number of unique goods
    n = len(all_warehouses)  # number of warehouses
    
    # Initialize matrices
    A1 = np.zeros((m, n, k))
    A2 = np.zeros((m, k))
    A3 = np.zeros((n, k))
    # W1 = 1 / np.arange(1, m+1)  # We consider the priority of orders to be inversely proportional to their order
    # W2 = 1 / np.arange(1, n+1)  # We consider the priority of warehouses to be inversely proportional to their order
    W1 = np.arange(m, 0, -1) / m * 0.3 + 0.7  # We consider the priority of orders to decrease by a fixed interval
    W2 = np.arange(n, 0, -1) / n * 0.3 + 0.7  # We consider the priority of warehouses to decrease by a fixed interval
   
    for i, order in enumerate(json_data['spdd']):
        good_id = all_goods.index(order['spnm'])
        A2[i, good_id] = order['sl']
        for j, ckdata in enumerate(order['ckdata']):
            A1[i, j, good_id] = ckdata['dwyssj']
    
    for warehouse in json_data['ck']:
        warehouse_id = list(warehouse.keys())[0]
        if warehouse_id in all_warehouses:
            i = all_warehouses.index(warehouse_id)
            for good in warehouse[warehouse_id]:
                good_id = all_goods.index(good['spnm'])
                A3[i, good_id] = good['sl']

    order_list = json_data['spdd']
    warehouse_list = all_warehouses
    goods_list = all_goods
    
    return A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list, goods_dict

if __name__=='__main__':
    with open('data/data_5.txt', 'r') as f:
        json_data = json.load(f)
    A1, A2, A3, W1, W2, order_list, warehouse_list, goods_list, goods_dict = json_to_matrices(json_data)
    print(order_list)
    print(warehouse_list)
    print(goods_list)
    print(goods_dict)

# fix this code, 
# currently, `all_warehouses = [data['cknm'] for order in json_data['spdd'] for data in order['ckdata']]`
# is not correct, because it count the warehouse with same cknm(warehous id) multiple times