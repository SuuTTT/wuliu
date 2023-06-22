import json
import os
import glob
import random

def generate_test_data(path, num_orders=10, num_spnms=5, num_warehouses=3):
    orders = {"Spdd": []}
    warehouse_names = [f"WH{i+1}" for i in range(num_warehouses)]
    spnms = [f"AUX{i+1}" for i in range(num_spnms)]

    for i in range(num_orders):
        order = {
            "ddnm": str(i + 1),
            "qynm": str(random.randint(100, 999)),
            "spnm": random.choice(spnms),
            "sl": random.randint(1, 10),
            "lg": "个",
            "zwdpwcsj": f"2023-06-{random.randint(25, 30)}T00:00:00",
            "jd": 39.913818,
            "wd": 116.363625,
            "ckdata": [
                {
                    "cknm": random.choice(warehouse_names),
                    "pfwhnm": "BOX1",
                    "yscb": random.uniform(1.0, 2.0)
                },
                {
                    "cknm": random.choice(warehouse_names),
                    "pfwhnm": "BOX2",
                    "yscb": random.uniform(1.0, 2.0)
                }
            ]
        }
        orders["Spdd"].append(order)

    existing_files = glob.glob(os.path.join(path, 'orders_data_*.json'))  
    max_index = max(int(file.split('_')[-1].split('.')[0]) for file in existing_files) if existing_files else 0

    filename = os.path.join(path, f'orders_data_{max_index+1}.json')

    with open(filename, 'w') as f:
        json.dump(orders, f, indent=4)

generate_test_data('./data/', num_orders=4, num_spnms=4, num_warehouses=6)
