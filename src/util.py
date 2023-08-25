import numpy as np
import os

def default_int64_handler(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


def generate_test_data(num_orders, num_warehouses, max_demand, max_inventory, exceed_inventory=False):
    X = np.random.randint(1, 5, size=(num_orders, num_warehouses))
    Y = np.random.randint(1, max_demand, size=(num_orders,))
    
    if exceed_inventory:
        total_demand = Y.sum()
        max_possible_inventory = total_demand - 1
        Z = np.random.randint(1, min(max_inventory, max_possible_inventory + 1), size=(num_warehouses,))
    else:
        Z = np.random.randint(1, max_inventory, size=(num_warehouses,))
    
    priority_order = np.random.permutation(num_orders)
    return X, Y, Z, priority_order

def save_test_data(filename, *args):
    if len(args) == 4 and all(isinstance(arg, (list, np.ndarray, tuple)) for arg in args[:-1]):
        # assuming the first scenario where you have X, Y, Z, and priority_order
        X, Y, Z, priority_order = args
        np.savez(filename, X=X, Y=Y, Z=Z, priority_order=priority_order)
    elif len(args) == 1 and isinstance(args[0], dict):
        # assuming the second scenario where you have test_data
        test_data = args[0]
        with open(filename, 'w') as f:
            json.dump(test_data, f, default=default_int64_handler)
    else:
        raise ValueError("Invalid arguments provided")


def load_test_data(filename):
    _, ext = os.path.splitext(filename)
    if ext == '.npz':
        data = np.load(filename)
        X = data['X']
        Y = data['Y']
        Z = data['Z']
        priority_order = data['priority_order']
        return X, Y, Z, priority_order
    elif ext == '.json':
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


import json
import numpy as np

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
    all_warehouses = []
    for order in json_data['spdd']:
        for data in order['ckdata']:
            if data['cknm'] not in all_warehouses:
                all_warehouses.append(data['cknm'])

    # Initialize matrices
    A1 = np.zeros((m, len(all_warehouses)))  # transportation time matrix
    A2 = np.zeros(m)                          # demand matrix
    A3 = np.zeros(len(all_warehouses))       # inventory matrix
    
    # Create a priority order list for orders
    priority_order = np.arange(m, 0, -1).tolist()
    
    for i, order in enumerate(json_data['spdd']):
        A2[i] = order['sl']
        for ckdata in order['ckdata']:
            j = all_warehouses.index(ckdata['cknm'])
            A1[i, j] = ckdata['dwyssj']
    
    for warehouse in json_data['ck']:
        warehouse_id = list(warehouse.keys())[0]
        if warehouse_id in all_warehouses:
            i = all_warehouses.index(warehouse_id)
            for good in warehouse[warehouse_id]:
                A3[i] += good['sl']

    order_list = json_data['spdd']
    warehouse_list = all_warehouses
    
    return A1, A2, A3, priority_order, order_list, warehouse_list, goods_dict


def generate_test_data_json(num_orders, num_warehouses, max_demand, max_inventory, exceed_inventory=False):
    X = np.random.randint(1, 5, size=(num_orders, num_warehouses))
    Y = np.random.randint(1, max_demand, size=(num_orders,))
    
    if exceed_inventory:
        total_demand = Y.sum()
        max_possible_inventory = total_demand - 1
        Z = np.random.randint(1, min(max_inventory, max_possible_inventory + 1), size=(num_warehouses,))
    else:
        Z = np.random.randint(1, max_inventory, size=(num_warehouses,))
    
    priority_order = np.random.permutation(num_orders)
    
    # Product id remains consistent
    product_id = "0030000000963"
    
    # Generate JSON format data
    spdd = []
    for i in range(num_orders):
        order_data = {
            "spnm": product_id,
            "wd": 32.2087,
            "ckdata": [{"cknm": f"warehouse{j}", "dwyssj": int(X[i][j])} for j in range(num_warehouses)],
            "ddnm": f"order{i}",
            "qynm": f"91020{i}",
            "zwdpwcsj": "2023-06-23T08:26:00",
            "sl": Y[i],
            "jd": 119.1611
        }
        spdd.append(order_data)
    
    ck = []
    for i in range(num_warehouses):
        warehouse_data = {
            f"warehouse{i}": [{
                "spnm": product_id,
                "sl": Z[i],
                "lg": "枚"
            }]
        }
        ck.append(warehouse_data)
    
    test_data = {
        "spdd": spdd,
        "ck": ck,
        "spmzd": 1,
        "dpsx": "先进先出"
    }
    
    return test_data, X, Y, Z, priority_order
