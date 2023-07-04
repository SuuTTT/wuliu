import numpy as np
import json
from util import json_to_matrices

from flask import Flask, request, jsonify
import json
import numpy as np

app = Flask(__name__)
from optimizer import logistics_distribution
@app.route('//getZytpcl', methods=['POST'])
def api_logistics_distribution():
    data = request.get_json()

    # Use the json_to_matrices function to convert the JSON data into matrices
    X, Y, Z, O, W, order_list, warehouse_list, goods_list,goods_dict = json_to_matrices(data)

    # Call the logistics_distribution function
    result = logistics_distribution(X, Y, Z, O, W, order_list, warehouse_list, goods_list,goods_dict)

    # Convert the returned result to JSON format
    #result_json = jsonify(result)

    return result

if __name__ == "__main__":
    #app.run(host=debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)