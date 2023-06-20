from util import *
from optimizer import *
from flask import Flask, request, jsonify
import random
import copy
import math


app = Flask(__name__)

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    orders = request.get_json()  # get data from POST request
    #orders = data['orders']
    strategies = []
    solution = simulated_annealing(orders)
    if solution is None:
        return jsonify({"code": -1, "data": {}, "message": "无推荐调配策略！"})
    solution = format_solution(solution)
    
    
    return jsonify({"code": 200, "data": solution, "message": "推荐调配策略！"})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
