#api_test.py
import requests
import json
from datetime import datetime, timedelta
url = "http://localhost:8080/getZytpcl"

data={"Spdd":[
     {
         "ddnm": "1",
         "qynm": "123",
         "spnm": "AUX",
         "sl": 5,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },      {
         "ddnm": "6",
         "qynm": "678",
         "spnm": "B",
         "sl": 14,
         "lg": "个",
         "zwdpwcsj": (datetime.fromisoformat("2023-06-30T00:00:00") + timedelta(hours=60)).isoformat(),
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      }
   
	],
   "spmzd": 0.95,
   "dpsx": "先进先出"
}


#data=given_data
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

try:
    print(response.json())
except json.JSONDecodeError:
    print("Empty response, no JSON to decode")

