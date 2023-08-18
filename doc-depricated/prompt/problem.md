## 1 transform order to strategy

### prompt
write a parser to transform order to strategy.

---

order :

```json
{
  "Spdd": [
    {
      "ddnm": "订单内码",
      "qynm": "提交商品订单企业内码",
      "spnm": "商品内码",
      "sl": "商品数量",
      "lg": "量纲",
      "zwdpwcsj": "最晚商品调配完成时间",
      "ckdata": [
        {
          "cknm": "仓库内码",
          "pfwhnm": "剖分网盒内码",
          "yscb": 6.0
        },
        {
          "cknm": "仓库内码",
          "pfwhnm": "剖分网盒内码",
          "yscb": 6.0
        }
      ]
    }
  ],
}

---

strategy

```json
{
  "code": 200,
  "data": [
    {
      "cknm": "仓库内码",
      "qynm": "企业内码",
      "spnm": "商品内码",
      "xqsj": "需求时间",
      "cb": "总调配成本",
      "sl": "分配的数量",
      "lg": "单位",
      "jd": "经度",
      "wd": "纬度",
      "ddnm": "订单内码"
    }
  ]
}
```

## 2 get the xyl of all warehouse by calling get_warehouse_inventory

get the xyl of all warehouse by calling get_warehouse_inventory

iterate all strategies(list of dict) to get all spnm 

and then call get_warehouse_inventory to get the xyl of all warehouse

save the xyl of all warehouse to a dictionary

---
def get_warehouse_inventory(spnm, zwkssj):
    """
    return a dictionary of {warehouse:inventory} for a specific product
    ignore zwkssj since this function is only called once when initializing the warehouse inventory
    """
    url = ckylcxByUTC_URL
    payload = {
        "spxqxx": [
            {
                "spnm": spnm,
                "zwkssj": zwkssj
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json().get('data', [])
        warehouse_inventory = {}
        for item in data:
            ckkcsj_vos = item.get('ckkcsj VOS', [])
            for vos in ckkcsj_vos:
                ckkcvos = vos.get('ckkcvos', [])
                for ckkcvo in ckkcvos:
                    cknm = ckkcvo.get('cknm')
                    xyl = ckkcvo.get('xyl')
                    if cknm and xyl is not None:  # to ensure both keys exist in the dictionary
                        warehouse_inventory[cknm] = xyl
        return warehouse_inventory
    else:
        return None

## simulate annealing
### prompt
use simulated annealing to optimize the strategies
the strategies is of the form of list of dict as follows

```json
[
    {
      "cknm": "仓库内码",
      "qynm": "企业内码",
      "spnm": "商品内码",
      "xqsj": "需求时间",
      "ksbysj": "开始搬运时间",
      "jsbysj": "结束搬运时间",
      "cb": "总调配成本",
      "sl": "分配的数量",
      "lg": "单位",
      "jd": "经度",
      "wd": "纬度",
      "ddnm": "订单内码"
    }
]
```
a strategy can be interpreted as "it takes 'cb' hours to deliver 'sl' of 'spnm' from 'cknm' to 'qynm'"



the objective function is to minimize the total cost of all strategies and the cost of a strategy is 'cb'

a strategy is valid if 
1. the sum of 'sl' of strategies of the same 'ddnm' is equal or greater than the 'sl' of the order of that 'ddnm'
2.  the sum of 'sl' of strategies of the same 'cknm' and 'spnm' is equal or less than the 'xyl' of the warehouse of that 'cknm' and 'spnm'.
3.  the time interval between 'ksbysj' and 'jsbysj' is not overlapped with any other strategies of the same 'cknm'

note that the 'ksbysj' and 'jsbysj' of a strategy is calculated by the following rules:  ksbysj = zwdpwcsj - ztpsj, jsbysj = zwdpwcsj-yscb, where yscb is strategy['cb'] and ztpsj is obtained by calling get_warehouse_inventory: ztpsj= get_total_dispatch_cost(spnm, ckdata.get("cknm"), jd, wd, sl, lg). note that spnm, cknm, jd, wd, sl, lg are all from that strategy
