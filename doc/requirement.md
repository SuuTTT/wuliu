

## 题目：库存调配最优化问题（退火算法）

### 1. 描述

你是一家大型电商公司的资深算法工程师，请实现一个接口函数（@app.route("/getZytpcl", methods=['POST'])  def getZytpcl()# 获取最优调配策略）负责从多个仓库运送多种商品给多个用户的以满足多个客户订单的需求。你的目标是在满足所有订单需求，时间不冲突和库存充足约束下，尽可能降低整体的物流成本。



### 2. 输入

**1. 订单列表**（通过req = request.json从请求中获取）：


```
//一个例子
{
   "Spdd":[  
      {
         "ddnm": "1", // 订单ID
         "qynm": "123", // 提交订单的企业ID
         "spnm": "AUX", // 商品ID
         "sl": 5, // 商品数量
         "lg": "个", // 单位
         "zwdpwcsj": "2023-06-30T00:00:00", // 完成调配的截止时间
         "jd": 39.913818, // 经度
         "wd": 116.363625, // 纬度
         "ckdata": [ 
            {
               "cknm":"WH1", // 仓库ID
               "pfwhnm":"BOX1", // 剖分网格仓库ID
               "yscb": 2.0 // 运输成本
            },
            {
               "cknm":"WH2", // 仓库ID
               "pfwhnm":"BOX2", // 剖分网格仓库ID
               "yscb": 1.0 // 运输成本
            }
         ]
      }
      // ...更多订单
   ]
}

```
- 约束涉及的属性是：对某种商品的需求量以及这个订单的最晚配送完成时间。

- 该订单的ckdata包括了可以为该订单供货的仓库的信息，剖分网格是用来标定仓库地理位置的。你需要从公司的这几个仓库中选择若干仓库来满足该订单。

- 另外，这里的经纬度用来唯一确定客户的地理位置。在后面查询成本时会用到。

**2. 运输成本** 通过已经实现的def get_total_costs(order,ckdata):获得，其返回值为形如{"code": 200, "data": 36.0}的json。表示从特定仓库（由经纬度确定）运输特定数量商品到特定客户的运输总成本（出库时间+运输成本）。

```
def get_total_costs(dingdan,ckdata):
    url = 'http://localhost:8000/sptp/queryYscb'
    payload = {
        "spnm": dingdan["spnm"],  # 商品内码
        "cknm": ckdata["cknm"],  # 仓库内码
        "jd": dingdan["jd"],  # 经度
        "wd": dingdan["wd"],  # 纬度
        "sl": dingdan["sl"],  # 商品数量
        "lg": dingdan["lg"]  # 单位
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
```


**3. 仓库的余量**，通过已经实现的def get_warehouse_stocks(dingdan)函数获取，返回的是一个json格式的响应，包含了指定商品在不同仓库的库存量。

```
# 获取仓库库存
def get_warehouse_stocks(dingdan):
    print("在获取仓库库存函数中------------")
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    
    # 构建商品详情信息列表
    spxqxx = []
    for order in dingdan:
        spxqxx.append({
            "spnm": order["spnm"],
            "zwkssj": ... #最晚开始时间(用订单需求时间减去调配成本)。
        })
        
    payload = {
        "spxqxx": spxqxx
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
//response.json的一个实际例子：
{
        "code": 200, 
        "data": [
            {
                "ckkcsjVOS": [  #仓库库存时间
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
                "spnm": "A"  # 商品内码
            },//...其他商品的库存信息]}
```
- 不同时间节点的在各个仓库中的库存信息，用于计算库存约束

## 约束

a. The total quantity of goods assigned to an order must be greater than or equal to the order's demand.

b. The total quantity of goods assigned from a warehouse should not exceed the warehouse's available stocks（对应 xyl #现有量）. 如果订单的需求量超过单个仓库的库存量，代码将会继续寻找下一个仓库。

c. 同一仓库同一时间段只能出货同一商品。举例来说，首先定义开始搬运时间=最晚商品调配完成时间（Spdd.zwdpwcsj）-总调配时间（queryYscb接口查询获取）
结束搬运时间=最晚商品调配完成时间（Spdd.zwdpwcsj）-运输时间（Spdd.ckData.yscb）。
假设A订单的开始搬运时间为6月6日12：00结束搬运时间为18：00；B订单的开始搬运时间为6月6日14：00，由于时间冲突，B订单无法使用A仓库.  


d. 严格按照订单顺序进行优先级分派，即保证在前面的订单尽早 尽可能满足。（不要按时间排序）

## 

## 输出

返回值是一个JSON对象的列表。每个JSON对象包含以下字段：

"cknm": 一个代表仓库内码的字符串。
"qynm": 提交订单的企业ID，类型为字符串。
"spnm": 商品内码，类型为字符串。
"sl": 商品数量，类型为数字。
"lg": 商品的单位，类型为字符串。
"jd": 经度，类型为数字。
"wd": 纬度，类型为数字。
"ddnm": 订单内码，类型为字符串。
"xqsj": 需求时间，这是提交订单的时间，类型为字符串或日期时间类型。
"cb": 订单的总成本，类型为数字。


## 任务

扩写下面函数，解决这个物流问题。
```
@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    req = request.json  # 获取请求中的 JSON 数据

    results = []  # 创建一个空列表来保存结果

    return jsonify(results)  # 将结果作为 JSON 返回
```


