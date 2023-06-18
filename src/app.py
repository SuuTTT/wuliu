from flask import Flask, request,jsonify
from optimizer import simulated_annealing
from util import *
app = Flask(__name__)

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    try:
        # 步骤一：从请求中提取订单信息
        orders = get_orders_from_request(request)
        
        # 初始化优化结果
        result = []
        
        # 步骤二：对每个订单进行处理
        for order in orders:
            # 获取仓库库存信息
            warehouse_stocks = get_warehouse_stocks(order)
            
            # 计算各个仓库的运输成本
            costs = []
            for ckdata in order["ckdata"]:
                cost = get_total_costs(order, ckdata)
                costs.append((ckdata["cknm"], cost["data"]))
            
            # 调用模拟退火算法进行优化
            optimized_order = simulated_annealing(order, warehouse_stocks, costs)
            
            # 添加到优化结果中
            result.append(optimized_order)
        
        # 步骤三：处理优化结果
        return jsonify({"code": 200, "data": result})
    
    except Exception as e:
        # 使用指定的错误返回格式
        return jsonify({"code": -1, "data": {}, "message": str(e)})
