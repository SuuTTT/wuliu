# 测试数据
request_data = {
    "Spdd": [
        {
            "ddnm": "order001",
            "qynm": "company001",
            "spnm": "AUX",
            "sl": 10.0,
            "lg": "kg",
            "zwdpwcsj": "2023-06-30T00:00:00Z",
            "ckdata": [
                {
                    "cknm": "WH1",
                    "pfwhnm": "grid001",
                    "yscb": 6.0,
                    "jd": 117.3,
                    "wd": 39.9
                },
                {
                    "cknm": "WH2",
                    "pfwhnm": "grid002",
                    "yscb": 8.0,
                    "jd": 116.4,
                    "wd": 39.9
                }
            ]
        },
        {
            "ddnm": "order002",
            "qynm": "company002",
            "spnm": "B",
            "sl": 20.0,
            "lg": "kg",
            "zwdpwcsj": "2023-07-01T00:00:00Z",
            "ckdata": [
                {
                    "cknm": "WH1",
                    "pfwhnm": "grid001",
                    "yscb": 6.0,
                    "jd": 117.3,
                    "wd": 39.9
                },
                {
                    "cknm": "WH2",
                    "pfwhnm": "grid002",
                    "yscb": 8.0,
                    "jd": 116.4,
                    "wd": 39.9
                }
            ]
        }
    ],
}
import requests
import json

url = "http://localhost:8080/getZytpcl"
headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(request_data))
print(response.json())
