import numpy as np
import json
import os

def generate_test_data_json(num_orders, num_warehouses, max_demand, max_inventory, exceed_inventory=False):
    X = np.random.randint(1, 5, size=(num_orders, num_warehouses))
    Y = np.random.randint(1, max_demand, size=(num_orders,))
    
    if exceed_inventory:
        total_demand = Y.sum()
        max_possible_inventory = total_demand - 1
        Z = np.random.randint(1, min(max_inventory, max_possible_inventory + 1), size=(num_warehouses,))
    else:
        Z = np.random.randint(1, max_inventory, size=(num_warehouses,))
    
    priority_order = np.random.permutation(num_orders).tolist()
    
    # Convert matrices and priority order to JSON format
    test_data = {
        "spdd": [],
        "ck": []
    }
    
    for i in range(num_orders):
        order_data = {
            "spnm": "0030000000963",
            "ckdata": [],
            "ddnm": f"168482973997d659e015cc{i}",
            "sl": Y[i]
        }
        for j in range(num_warehouses):
            ckdata = {
                "cknm": f"76010046{j}",
                "dwyssj": int(X[i][j])
            }
            order_data["ckdata"].append(ckdata)
        test_data["spdd"].append(order_data)
    
    for j in range(num_warehouses):
        warehouse_data = {
            f"76010046{j}": [
                {
                    "spnm": "0030000000963",
                    "sl": Z[j],
                    "lg": "枚"
                }
            ]
        }
        test_data["ck"].append(warehouse_data)
    
    return test_data, X, Y, Z, priority_order

def save_test_data(filename, test_data):
    with open(filename, 'w') as f:
        json.dump(test_data, f, default=default_int64_handler)

def default_int64_handler(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

def load_test_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def json_to_matrices(json_data):
    m = len(json_data['spdd'])  # number of orders

    # Create a dictionary to map goods to units
    goods_dict = {}
    for warehouse in json_data['ck']:
        warehouse_id = list(warehouse.keys())[0]
        for good in warehouse[warehouse_id]:
            if good['spnm'] not in goods_dict:
                goods_dict[good['spnm']] = good['lg']
    
    all_warehouses = sorted(list(set([data['cknm'] for order in json_data['spdd'] for data in order['ckdata']])))
    n = len(all_warehouses)  # number of warehouses
    
    # Initialize matrices
    A1 = np.zeros((m, n))
    A2 = np.zeros((m,))
    A3 = np.zeros((n,))
   
    for i, order in enumerate(json_data['spdd']):
        A2[i] = order['sl']
        for ckdata in order['ckdata']:
            j = all_warehouses.index(ckdata['cknm'])
            A1[i, j] = ckdata['dwyssj']
    
    for warehouse in json_data['ck']:
        warehouse_id = list(warehouse.keys())[0]
        if warehouse_id in all_warehouses:
            j = all_warehouses.index(warehouse_id)
            for good in warehouse[warehouse_id]:
                A3[j] = good['sl']

    order_list = [order['ddnm'] for order in json_data['spdd']]
    warehouse_list = all_warehouses
    
    return A1, A2, A3, order_list, warehouse_list, goods_dict


def save_results(filename, allocation_matrix, max_transport_time):
    with open(filename, 'w') as f:
        data = {
            'allocation_matrix': allocation_matrix.tolist(),  # Assuming it's a numpy array. If it's a list, just use allocation_matrix.
            'max_transport_time': max_transport_time
        }
        json.dump(data, f)
