import random
import math
from util import *

# 贪婪选择
def greedy_select(stocks, order, costs):
    allocation = []
    total_cost = 0
    total_quantity = 0
    for ckdata, cost in costs:
        if total_quantity >= order["sl"]:
            break
        quantity = min(order["sl"] - total_quantity, stocks[ckdata["cknm"]])
        total_quantity += quantity
        total_cost += quantity * cost
        allocation.append({
            "cknm": ckdata["cknm"],
            "qynm": order["qynm"],
            "spnm": order["spnm"],
            "sl": quantity,
            "lg": order["lg"],
            "jd": order["jd"],
            "wd": order["wd"],
            "ddnm": order["ddnm"],
            "cb": quantity * cost
        })
    return allocation, total_cost

# 随机选择
def random_select(stocks, order, costs):
    allocation = []
    total_cost = 0
    total_quantity = 0
    random.shuffle(costs)
    for ckdata, cost in costs:
        if total_quantity >= order["sl"]:
            break
        quantity = min(order["sl"] - total_quantity, stocks[ckdata["cknm"]])
        total_quantity += quantity
        total_cost += quantity * cost
        allocation.append({
            "cknm": ckdata["cknm"],
            "qynm": order["qynm"],
            "spnm": order["spnm"],
            "sl": quantity,
            "lg": order["lg"],
            "jd": order["jd"],
            "wd": order["wd"],
            "ddnm": order["ddnm"],
            "cb": quantity * cost
        })
    return allocation, total_cost

# 退火过程
def annealing_process(order, warehouse_stocks, costs, temp, cool, iters):
    best_alloc, best_cost = greedy_select(warehouse_stocks, order, costs)
    alloc, cost = best_alloc, best_cost
    while temp > 0.1:
        for _ in range(iters):
            new_alloc, new_cost = random_select(warehouse_stocks, order, costs)
            delta = new_cost - cost
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
                alloc, cost = new_alloc, new_cost
                if cost < best_cost:
                    best_alloc, best_cost = alloc, cost
        temp *= cool
    return best_alloc

# 模拟退火算法
def simulated_annealing(order, warehouse_stocks, costs, temp=10000.0, cool=0.95, iters=100):
    # 初始化库存信息
    stocks = {stock["cknm"]: stock["xyl"] for stock in warehouse_stocks["data"][0]["ckkcsjVOS"][0]["ckkcvos"]}
    
    # 排序仓库成本
    costs.sort(key=lambda x: x[1])
    
    # 进行退火过程
    best_alloc = annealing_process(order, stocks, costs, temp, cool, iters)
    
    # 返回最佳分配
    return best_alloc
