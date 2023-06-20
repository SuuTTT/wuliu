#api_mock.py
from flask import Flask, request, jsonify
import os


app = Flask(__name__)

@app.route("/sptp/queryYscb", methods=['POST'])
def mock_queryYscb():
    req = request.json  # 获取请求中的 JSON 数据
    unit_cost = 1  # 模拟每件商品的运输成本
    total_cost = unit_cost * req["sl"]  # 总的运输成本等于每件商品的运输成本乘以商品数量
    return jsonify({"code": 200, "data": total_cost+2})  # 返回总的运输成本


@app.route("/sptp/ckylcxByUTC", methods=['POST'])
def mock_ckylcxByUTC():
    return jsonify({
        "code": 200, 
        "data": [
            {
                "ckkcsjVOS": [
                    {
                        "sjjd": "2023-06-30T00:00:00",
                        "ckkcvos": [
                            {
                                "cknm": "WH1",
                                "xyl": 8.0
                            },
                            {
                                "cknm": "WH2",
                                "xyl": 8.0
                            }
                        ]
                    }
                ],
                "spnm": "AUX"
            }
        ]
    })
    # 这里返回模拟数据，模拟仓库库存信息
    return jsonify({
        "code": 200, 
        "data": [
            {
                "ckkcsjVOS": [ # 仓库库存时间
                    {
                        "sjjd": "2023-06-30T00:00:00",  # 时间节点
                        "ckkcvos": [
                            {
                                "cknm": "WH1",  # 仓库内码
                                "xyl": 10.0  # 现有量
                            },
                            {
                                "cknm": "WH2",  # 仓库内码
                                "xyl": 8.0  # 现有量
                            }
                        ]
                    }
                ],
                "spnm": "AUX"  # 商品内码
            },
            {
                "ckkcsjVOS": [
                    {
                        "sjjd": "2023-06-30T00:00:00",  # 时间节点
                        "ckkcvos": [
                            {
                                "cknm": "WH1",  # 仓库内码
                                "xyl": 8.0  # 现有量
                            },
                            {
                                "cknm": "WH2",  # 仓库内码
                                "xyl": 6.0  # 现有量
                            }
                        ]
                    }
                ],
                "spnm": "B"  # 商品内码
            }
        ]
    })

if __name__ == "__main__":
    app.run(port=8000,debug=True)
