from util import get_warehouse_stocks,get_total_costs
from flask import Flask, request, jsonify
import random
import copy
import math

app = Flask(__name__)

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    req = request.json  # 获取请求中的 JSON 数据

    # 1. 生成所有可能的调配策略
    strategies = generate_strategies(req['Spdd'])

    # 2. 进行模拟退火
    best_strategies = simulated_annealing(strategies)

    # 3. 解码最优策略并返回结果
    results = decode_strategies(best_strategies)

    return jsonify(results)  # 将结果作为 JSON 返回

def generate_strategies(Spdd):
    strategies = []
    for order in Spdd:
        for warehouse in order['ckdata']:
            strategies.append({'cknm': warehouse['cknm'], 'order': order})
    return strategies

from tqdm import tqdm

def simulated_annealing(strategies):
    T = 100.0  # Initial temperature
    T_min = 0.01  # Minimum temperature
    alpha = 0.9  # Annealing rate
    best_strategies = strategies
    best_cost = calculate_total_cost(strategies)

    # Initialize progress bar with total iterations as the initial temperature to the minimum temperature
    pbar = tqdm(total=int(T/T_min))
    while T > T_min:
        i = 1
        while i <= 10:  # Each temperature is iterated 100 times
            new_strategies = neighbour(best_strategies)
            new_cost = calculate_total_cost(new_strategies)
            if new_cost < best_cost:
                best_strategies = new_strategies
                best_cost = new_cost
            elif random.uniform(0, 1) < math.exp((best_cost - new_cost) / T):  # Metropolis criteria
                best_strategies = new_strategies
                best_cost = new_cost
            i += 1
        T = T * alpha  # Cool down
        pbar.update(int(1/alpha))  # Update the progress bar
    pbar.close()  # Close the progress bar when done
    return best_strategies

def neighbour(strategies):
    # 随机选择两个策略，然后交换它们的位置
    new_strategies = copy.deepcopy(strategies)
    i = random.randint(0, len(new_strategies) - 1)
    j = random.randint(0, len(new_strategies) - 1)
    new_strategies[i], new_strategies[j] = new_strategies[j], new_strategies[i]
    return new_strategies

def calculate_total_cost(strategies):
    total_cost = 0
    for strategy in strategies:
        for ckdata in strategy['order']['ckdata']:
            #print(strategy, ckdata)
            response = get_total_costs(strategy['order'], ckdata)
            total_cost += response['data']
    return total_cost


def decode_strategies(strategies):
    results = []
    for strategy in strategies:
        for ckdata in strategy['order']['ckdata']:
            result = {
                "cknm": ckdata["cknm"],
                "qynm": strategy["order"]["qynm"],
                "spnm": strategy["order"]["spnm"],
                "sl": strategy["order"]["sl"],
                "lg": strategy["order"]["lg"],
                "jd": strategy["order"]["jd"],
                "wd": strategy["order"]["wd"],
                "ddnm": strategy["order"]["ddnm"],
                "xqsj": strategy["order"]["zwdpwcsj"],
                "cb": get_total_costs(strategy['order'], ckdata)['data']
            }
            results.append(result)
    return results


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
