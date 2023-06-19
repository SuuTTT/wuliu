from flask import Flask, request,jsonify
from optimizer import simulated_annealing
from util import *
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    #try:
        # 从请求中获取订单数据
        Spdd = request.json['Spdd']
        
        # 初始化最优解列表
        optimized_solution = []

        # 设置模拟退火算法的参数
        T_initial = 100
        T_final = 0.1
        alpha = 0.9
        max_iter = 1000

        # 对每个订单进行处理
        for order in Spdd:
            # 获取订单详情
            ddnm = order['ddnm']
            qynm = order['qynm']
            spnm = order['spnm']
            sl = order['sl']
            lg = order['lg']
            zwdpwcsj = order['zwdpwcsj']
            ckdata = order['ckdata']

            # 获取仓库库存信息
            warehouse_inventory = get_warehouse_inventory(spnm, zwdpwcsj)
            
            # 对仓库库存进行处理，计算最优调配策略
            for warehouse in warehouse_inventory['data']:
                for ck in ckdata:
                    if warehouse['cknm'] == ck['cknm']:
                        dispatch_cost_info = get_total_dispatch_cost(spnm, ck['cknm'], ck['jd'], ck['wd'], sl, lg)
                        cb = dispatch_cost_info['data']['zcb']  # 获取总成本
                        ksbysj = dispatch_cost_info['data']['ksbysj']  # 开始搬运时间
                        jsbysj = dispatch_cost_info['data']['jsbysj']  # 结束搬运时间
                        jd = ck['jd']
                        wd = ck['wd']
                        sl = warehouse['kykcl']  # 仓库库存量
                        
                        # 记录调配策略
                        dispatch_policy = {
                            'cknm': ck['cknm'],
                            'qynm': qynm,
                            'spnm': spnm,
                            'xqsj': zwdpwcsj,
                            'ksbysj': ksbysj,
                            'jsbysj': jsbysj,
                            'cb': cb,
                            'sl': sl,
                            'lg': lg,
                            'jd': jd,
                            'wd': wd,
                            'ddnm': ddnm,
                        }
                        optimized_solution.append(dispatch_policy)
        # 返回最优调配策略
        return jsonify({"code": 200, "data": optimized_solution})
    
    # except Exception as e:
    #     # 使用指定的错误返回格式
    #     return jsonify({"code": -1, "data": {}, "message": str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
