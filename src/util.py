from flask import Flask, request, jsonify
from queue import PriorityQueue
import random
import copy
import requests
import math
app = Flask(__name__)
# 获取仓库库存
def get_warehouse_stocks(dingdan):
    print("在获取仓库库存函数中------------")
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    
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
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"在获取仓库库存函数中出现错误: {response.status_code}, {response.text}")

# 获取从坐标到仓库运输商品的总成本=出库时间+运输成本+提收成本（暂时不考虑）
def get_total_costs(dingdan,ckdata):
    url = 'http://localhost:8000/sptp/queryYscb'
    payload = {
        "spnm": dingdan["spnm"],  # 商品内码
        "cknm": ckdata["cknm"],  # 仓库内码
        "jd": dingdan["jd"],  # 经度
        "wd": dingdan["wd"],  # 纬度
        "sl": dingdan["sl"],  # 商品数量
        "lg": dingdan["lg"]  # 单位
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