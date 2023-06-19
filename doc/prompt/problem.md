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

## simulate