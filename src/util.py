import numpy as np
import json
import os


def validate_inputs(X, Y, Z):
    """
    Validates the input parameters for the product allocation problem.
    
    :param X: Transport Time Matrix (2D NumPy array)
    :param Y: Demand Array (1D NumPy array)
    :param Z: Stock Array (1D NumPy array)
    :return: A boolean value indicating the validity of the inputs and a message string.
    """
    # Check if X is a 2D array
    if X.ndim != 2:
        return False, "X must be a 2D array currently"
    
    # Check if Y and Z are 1D arrays
    if Y.ndim != 1 or Z.ndim != 1:
        return False, "Y and Z must be 1D arrays currently"
    
    # Check if the dimensions of X, Y, and Z are compatible
    rows_X, cols_X = X.shape
    if len(Y) != rows_X or len(Z) != cols_X:
        return False, "Dimensions of X, Y, and Z are not compatible"
    
    # Check if all elements are non-negative
    if np.any(X < 0) or np.any(Y < 0) or np.any(Z < 0):
        return False, "All elements in X, Y, and Z must be non-negative"
    
    return True, "Inputs are valid"


# note: the priority will always be 0,1,2,3... ;  that should make no harm since input insures the higher order at first.

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
   
    # Extracting data from the JSON to form the matrices
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

    # Order list can act as the priority order since the JSON contains orders in a specific sequence.
    # Note: This assumes the input json_data already has the orders in the desired priority.
    priority_order = [i for i, _ in sorted(enumerate([order['ddnm'] for order in json_data['spdd']]), key=lambda x: x[1])]
    
    order_list = [order['ddnm'] for order in json_data['spdd']]
    warehouse_list = all_warehouses
    
    return A1, A2, A3, order_list, warehouse_list, goods_dict, priority_order


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


import numpy as np
import json

class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)): 
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

    
def save_results(filename, allocation_matrix, max_transport_time):
    data = {
        'allocation_matrix': allocation_matrix,
        'max_transport_time': max_transport_time
    }

    # Try saving data
    with open(filename, 'w') as f:
        json.dump(data, f, cls=NumpyEncoder)


def append_data(test_data, source='generated', filename=None, num_orders=None, num_warehouses=None, max_demand=None, max_inventory=None, description=""):
    """
    Appends test data to the provided test data list.

    Args:
    - test_data (list): The list of existing test data cases.
    - source (str): 'generated' to generate new test data, 'file' to read from a file.
    - filename (str, optional): Name of the file from which the data is to be read, required if source='file'.
    - num_orders (int, optional): Number of orders for the generated data, required if source='generated'.
    - num_warehouses (int, optional): Number of warehouses for the generated data, required if source='generated'.
    - max_demand (int, optional): Maximum demand for the generated data, required if source='generated'.
    - max_inventory (int, optional): Maximum inventory for the generated data, required if source='generated'.
    - description (str): Description of the appended test data.

    Returns:
    - list: Updated test data list with the new data appended.
    """
    if source == 'generated':
        if not (num_orders and num_warehouses and max_demand and max_inventory):
            raise ValueError("For generated data, num_orders, num_warehouses, max_demand, and max_inventory must be provided.")

        generated_data, X, Y, Z, priority_order = generate_test_data_json(num_orders, num_warehouses, max_demand, max_inventory)

        test_case = {
            'X': X,
            'Y': Y,
            'Z': Z,
            'priority_order': priority_order,
            'description': description
        }

    elif source == 'file':
        if not filename:
            raise ValueError("Filename must be provided when source is set to 'file'.")

        with open(filename, 'r') as f:
            loaded_data = json.load(f)

        A1, A2, A3, order_list, warehouse_list, goods_dict,priority_order = json_to_matrices(loaded_data)

        test_case = {
            'X': A1,
            'Y': A2,
            'Z': A3,
            'priority_order': priority_order,
            'description': description
        }

    else:
        raise ValueError("Invalid source provided. Choose from 'generated' or 'file'.")

    test_data.append(test_case)
    return test_data



if __name__ == '__main__':
    # Ensure the "tmp/" directory exists
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    # 1. Generate test data
    test_data, X, Y, Z, priority_order = generate_test_data_json(10, 5, 50, 100)
    print("Generated Test Data:\n", test_data)
    
    # 2. Save generated data to a JSON file
    save_test_data("tmp/test_data.json", test_data)
    print("\nTest data saved to tmp/test_data.json")
    
    # 3. Load test data from the saved JSON file
    loaded_data = load_test_data("tmp/test_data.json")
    print("\nLoaded Test Data from tmp/test_data.json:\n", loaded_data)
    
    # 4. Convert the loaded JSON data back to matrices
    A1, A2, A3, order_list, warehouse_list, goods_dict, extracted_priority_order = json_to_matrices(loaded_data)
    print("\nConverted matrices from loaded JSON data:")
    print("A1:\n", A1)
    print("A2:\n", A2)
    print("A3:\n", A3)
    
    
    print("\nResults saved to tmp/results.json")
    # 5. Test data definitions
    test_data = [
        {
            'X': np.array([[4, 2], [3, 2]]),
            'Y': np.array([1, 1]),
            'Z': np.array([3, 4]),
            'priority_order': np.array([0, 1]),
            'description': "All orders can be satisfied, no priority needed"
        },
        {
            'X': np.array([[2, 8], [1, 4]]),
            'Y': np.array([10, 5]),
            'Z': np.array([5, 5]),
            'priority_order': np.array([0, 1]),
            'description': "Not all orders can be satisfied, and priority comes into play"
        },
        {
            'X': np.array([[1, 1], [1, 2]]),
            'Y': np.array([1, 1]),
            'Z': np.array([1, 1]),
            'priority_order': np.array([0, 1]),
            'description': "All orders can be satisfied, but not in a greedy manner"
        },
        {
            'X': np.array([[1], [0], [2]]),
            'Y': np.array([1, 1, 2]),
            'Z': np.array([2]),
            'priority_order': np.array([2, 1, 0]),
            'description': "Not all orders can be satisfied, and priority comes into play"
        },
        {
            'X': np.array([[1]]),
            'Y': np.array([1]),
            'Z': np.array([1]),
            'priority_order': np.array([0]),
            'description': "All orders can be satisfied, no priority needed"
        },
        {
            'X': np.array([[1, 1], [0, 0]]),
            'Y': np.array([1, 1]),
            'Z': np.array([1, 1]),
            'priority_order': np.array([1, 0]),
            'description': "Not all orders can be satisfied, but all warehouses can contribute to the high priority order"
        },
        {
            'X': np.array([[1., 4.],
                        [2., 2.],
                        [4., 2.],
                        [2., 1.],
                        [1., 4.]]), 
            'Y': np.array([46., 26.,  6., 27., 17.]),
            'Z': np.array([2., 18.]),
            'priority_order': np.array([3, 4, 1, 0, 2]),
            'description': "Complex case"
        }
    ]
    
    # 6.test data from generated and file
    # Example of appending generated data
    test_data = append_data(test_data, source='generated', num_orders=5, num_warehouses=3, max_demand=10, max_inventory=7, description="Generated data example")

    # Example of appending data from a file
    test_data = append_data(test_data, source='file', filename="tmp/test_data.json", description="Data loaded from file")

    # 7. Run and Save some results to a JSON file
    for i, case in enumerate(test_data):
        is_valid, message = validate_inputs(case['X'], case['Y'], case['Z'])
        print(f"Test case {i+1} ({case['description']}): {message}")
        
        save_results("tmp/results.json", A1, 5)

