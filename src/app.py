import numpy as np
import json
from util import json_to_matrices

from flask import Flask, request, jsonify
import json
import numpy as np

app = Flask(__name__)
from optimizer import logistics_distribution
@app.route('/api/logistics_distribution', methods=['POST'])
def api_logistics_distribution():
    data = request.get_json()
    A1, A2, A3, W1, W2 = json_to_matrices(data)
    
    # 调用logistics_distribution函数，这里假设函数已经定义，并接受相应的参数
    result = logistics_distribution(A1, A2, A3, W1, W2)
    
    # 将返回的结果转换为JSON格式
    result_json = jsonify(result)
    
    return result_json