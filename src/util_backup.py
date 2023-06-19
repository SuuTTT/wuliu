import json
from flask import Flask, request, jsonify
from queue import PriorityQueue
import random
import copy
import requests
import math
import requests
import logging
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

config = load_config()
queryYscb_URL = config.get('API', 'queryYscb')
ckylcxByUTC_URL = config.get('API', 'ckylcxByUTC')
app = Flask(__name__)


def get_warehouse_inventory(spnm, zwkssj):
    url = ckylcxByUTC_URL
    payload = {
        "spxqxx": [
            {
                "spnm": spnm,
                "zwkssj": zwkssj
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_total_dispatch_cost(spnm, cknm, jd, wd, sl, lg):
    url = queryYscb_URL
    payload = {
        "spnm": spnm,
        "cknm": cknm,
        "jd": jd,
        "wd": wd,
        "sl": sl,
        "lg": lg
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# 获取仓库库存
def get_warehouse_stocks(orders, transport_time):
    print("in get_warehouse_stocks function------------")
    print(orders)
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    
    # Construct the product details information list
    spxqxx = []
    for order in orders:
        
        zwdpwcsj = datetime.strptime(order["deadline"], '%Y-%m-%dT%H:%M:%S')
        
        # Compute total_dispatch_time by using get_total_costs
        total_dispatch_time = get_total_costs(order, order["warehouses"])["total_costs"]

        # Compute start and end times according to the definition
        start_dispatch_time = zwdpwcsj - timedelta(hours=total_dispatch_time)
        end_dispatch_time = zwdpwcsj - timedelta(hours=transport_time)

        spxqxx.append({
            "spnm": order["product_id"],
            "zwkssj": start_dispatch_time.strftime('%Y-%m-%dT%H:%M:%S'),
            #"zwdpwcsj": end_dispatch_time.strftime('%Y-%m-%dT%H:%M:%S')
        })
        
    payload = {
        "spxqxx": spxqxx
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()



def get_warehouse_stocks_(dingdan):
    url=queryYscb_URL
    if not dingdan:
        raise ValueError("订单列表不能为空")

    for order in dingdan:
        if "spnm" not in order or ("zwkssj" not in order and "zwdpwcsj" not in order):
            raise ValueError("每个订单都必须包含商品内码和至少一个时间字段")

    logging.info("在获取仓库库存函数中------------")

    # 构建商品详情信息列表
    spxqxx = []
    for order in dingdan:
        spxqxx.append({
            "spnm": order["spnm"],
            # 如果'最晚开始时间'不存在，使用'最晚调配完成时间'
            "zwkssj": order.get("zwkssj", order["zwdpwcsj"])
        })

    payload = {
        "spxqxx": spxqxx
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"在获取仓库库存函数中出现错误: {e}")
        return None

    data = response.json()
    if "code" not in data or "data" not in data:
        logging.error(f"返回的数据格式不正确: {data}")
        return None

    if data["code"] != 200:
        logging.error(f"在获取仓库库存函数中出现错误: {data['code']}, {data.get('message', '')}")
        return None

    logging.info(data)
    return data


# 获取从坐标到仓库运输商品的总成本=出库时间+运输成本+提收成本（暂时不考虑）
def get_total_costs(order, warehouse):
    print("in get_total_costs function------------")
    print(warehouse)
    url = 'http://localhost:8000/sptp/queryYscb'
    payload = {
        "spnm": order["product_id"],  # 商品内码
        "cknm": warehouse["id"],  # 仓库内码
        "jd": order["longitude"],  # 经度
        "wd": order["latitude"],  # 纬度
        "sl": order["quantity"],  # 商品数量
        "lg": order["unit"]  # 单位
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"在获取总成本函数中出现错误: {response.status_code}, {response.text}")

def get_orders_from_request(request):
    # 从请求中提取订单数据
    req = request.json  # 获取请求中的 JSON 数据
    # 对数据进行验证和预处理
    # 这里只是一个例子，你可能需要根据你的实际需求来实现
    if 'Spdd' not in req:
        raise ValueError("在获取订单中出现错误: missing 'Spdd'")
    return req['Spdd']

### for optimizer

from datetime import datetime, timedelta

def get_order_start_time(order):
    # The start time of the order is the "最晚商品调配完成时间" minus the "总调配时间"
    zwdpwcsj = datetime.strptime(order["zwdpwcsj"], "%Y-%m-%dT%H:%M:%S")
    total_time = timedelta(hours=order["total_time"])  # Assume "total_time" is a property of the order
    return zwdpwcsj - total_time

def get_order_end_time(order):
    # The end time of the order is the "最晚商品调配完成时间" minus the "运输时间"
    zwdpwcsj = datetime.strptime(order["zwdpwcsj"], "%Y-%m-%dT%H:%M:%S")
    transport_time = timedelta(hours=order["transport_time"])  # Assume "transport_time" is a property of the order
    return zwdpwcsj - transport_time


import requests
import logging
def get_initial_inventory(warehouse_id, all_orders):
    # Filter out the orders that are related to this warehouse
    related_orders = [order for order in all_orders if warehouse_id in [w["id"] for w in order["warehouses"]]]
    print(related_orders)
    
    # Find the warehouse information from the related order's "warehouses" field
    related_warehouse = next((w for w in related_orders[0]["warehouses"] if w["id"] == warehouse_id), None)
    
    if related_warehouse is None:
        raise Exception(f"No related warehouse found for warehouse_id {warehouse_id} in the related_orders")

    transport_time = related_warehouse["shipping_cost"]
    
    return get_warehouse_stocks(related_orders, transport_time)


def get_initial_schedules(warehouse_id):
    # There are no initial schedules for the warehouse
    return []

### parse


def parse_data(json_data):
    orders = []
    for order_data in json_data["Spdd"]:
        order = {
            "id": order_data["ddnm"],
            "company_id": order_data["qynm"],
            "product_id": order_data["spnm"],
            "quantity": order_data["sl"],
            "unit": order_data["lg"],
            "deadline": order_data["zwdpwcsj"],
            "longitude": order_data["jd"],  # 经度
            "latitude": order_data["wd"],  # 纬度
            "warehouses": [{ "id": ck["cknm"], "grid_id": ck["pfwhnm"], "shipping_cost": ck["yscb"] } for ck in order_data["ckdata"]]
        }
        orders.append(order)

    warehouses = { warehouse["id"]: {
        "grid_id": warehouse["grid_id"],
        "inventory": get_initial_inventory(warehouse["id"], orders),
        "schedules": get_initial_schedules(warehouse["id"]),
    } for order in orders for warehouse in order["warehouses"]}

    return orders, warehouses


from datetime import datetime

def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

import json

def read_orders_from_file(file_path):
    with open(file_path, 'r') as f:
        orders = json.load(f)
    return orders