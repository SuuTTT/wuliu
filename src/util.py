import json
from flask import Flask, request, jsonify
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

from datetime import datetime

def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')
import json

def get_total_dispatch_cost(spnm, cknm, jd, wd, sl, lg):
    """
    return data(double) directly 
    
    """
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
        return response.json().get('data')
    else:
        return None


def orders_to_strategies(orders):
    strategies = []

    for item in orders['Spdd']:
        ddnm = item.get("ddnm")
        qynm = item.get("qynm")
        spnm = item.get("spnm")
        sl = item.get("sl")
        lg = item.get("lg")
        jd = item.get("jd")
        wd = item.get("wd")
        zwdpwcsj = item.get("zwdpwcsj")
        zwdpwcsj = parse_date(zwdpwcsj)
        for ckdata in item.get("ckdata", []):
            strategy_item = {}
            strategy_item["ddnm"] = ddnm
            strategy_item["qynm"] = qynm
            strategy_item["spnm"] = spnm
            strategy_item["sl"] = sl
            strategy_item["lg"] = lg
            strategy_item["xqsj"] = zwdpwcsj
            strategy_item["cknm"] = ckdata.get("cknm")
            strategy_item["yscb"] = ckdata.get("yscb")
            strategy_item["jd"] = jd
            strategy_item["wd"] = wd
            #使用parse_date函数将字符串转换为datetime对象         
            yscb=ckdata.get("yscb")
            # 将float yscb转换可以和datetime对象相减的timedelta对象
            yscb=timedelta(hours=yscb)
            jsbysj = zwdpwcsj-yscb
            # “总调配时间” 通过调用get_total_dispatch_cost获得
            ztpsj= get_total_dispatch_cost(spnm, ckdata.get("cknm"), jd, wd, sl, lg)
            ztpsj=timedelta(hours=ztpsj)
            # 我们定义一个调配策略的“开始搬运时间”为“最晚商品调配完成时间”减去“总调配时间”，
            ksbysj = zwdpwcsj - ztpsj
            strategy_item["zwdpwcsj"] = zwdpwcsj
            strategy_item["ksbysj"] = ksbysj
            strategy_item["jsbysj"] = jsbysj
            strategy_item["cb"]=ztpsj
            strategies.append(strategy_item)

    return strategies




   
def get_warehouse_inventory(spnm, zwkssj):
    """
    spnm: 商品内码
    zwkssj(str): 最晚开始时间(yyyy-mm-ddThh:mm:ss)
    return a dictionary of {warehouse:inventory} for a specific product
    ignore zwkssj since this function is only called once when initializing the warehouse inventory
    """
    url = ckylcxByUTC_URL
    from datetime import datetime

    # suppose zwkssj is of datetime type, for instance:
    # zwkssj = datetime.now()

    # check if zwkssj is of datetime type
    if isinstance(zwkssj, datetime):
        zwkssj = zwkssj.strftime("%Y-%m-%dT%H:%M:%S")

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
        data = response.json().get('data', [])
        warehouse_inventory = {}
        for item in data:
            ckkcsj_vos = item.get('ckkcsjVOS', [])
            for vos in ckkcsj_vos:
                ckkcvos = vos.get('ckkcvos', [])
                for ckkcvo in ckkcvos:
                    cknm = ckkcvo.get('cknm')
                    xyl = ckkcvo.get('xyl')
                    if cknm and xyl is not None:  # to ensure both keys exist in the dictionary
                        warehouse_inventory[cknm] = xyl
        return warehouse_inventory
    else:
        return None

# not consider spnm
def get_all_warehouses_xyl(strategies, zwkssj):
    """
    Given a list of strategies, calls `get_warehouse_inventory` for each 'spnm' in each strategy.
    Returns a dictionary mapping each warehouse to its xyl.
    """
    all_warehouses_xyl = {}

    # Iterate over all strategies
    for strategy in strategies:
        # Get the 'spnm' value
        spnm = strategy.get('spnm')
        if spnm is not None:  # Ensure 'spnm' key exists in the dictionary
            # Call `get_warehouse_inventory` and get the warehouse inventory
            warehouse_inventory = get_warehouse_inventory(spnm, zwkssj)
            if warehouse_inventory is not None:  # Ensure valid response
                # Update the overall dictionary with the warehouse inventory
                for warehouse, xyl in warehouse_inventory.items():
                    if warehouse in all_warehouses_xyl:
                        all_warehouses_xyl[warehouse][spnm] = xyl
                    else:
                        all_warehouses_xyl[warehouse] = {spnm: xyl}
    return all_warehouses_xyl



import json

def read_orders_from_file(file_path):
    with open(file_path, 'r') as f:
        orders = json.load(f)
    return orders


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







