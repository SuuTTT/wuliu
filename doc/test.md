## 算法问题

题目：库存调配最优化问题测试数据正常

描述：

你是一家大型电商公司的软件测试员，负责测试算法，该算法负责调配公司的多个仓库库存以满足多个客户订单的需求。你的目标是通过选择从哪个仓库分配哪个商品给哪个订单，在满足时间和库存约束下，以尽可能降低整体的物流成本。

下面描述该算法

**输入数据包括：**
1 订单列表，每个订单包含对某种商品的特定需求量以及这个订单的最晚配送完成时间，你需要从公司的多个仓库中选择合适的仓库来满足这些订单。订单通过req = request.json得到：

```
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
               "pfwhnm":"BOX1", // 批发仓库ID
               "yscb": 2.0 // 运输成本
            },
            {
               "cknm":"WH2", // 仓库ID
               "pfwhnm":"BOX2", // 批发仓库ID
               "yscb": 1.0 // 运输成本
            }
         ]
      }
      // ...更多订单
   ]
}

```

2 从特定客户（用经纬度表示）到特定仓库的运输总成本。通过已经实现的def get_total_costs(order,ckdata):获得，其返回值为形如{"code": 200, "data": 36.0}的json

3 仓库的余量，每个仓库都有一定数量的各种商品， 通过已经实现的def get_warehouse_stocks(orders)获得 ，其返回值示例如下

```
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
            },...]}
```
4.  


**约束包括:**


a. The total quantity of goods assigned to an order must be greater than or equal to the order's demand.

b. The total quantity of goods assigned from a warehouse should not exceed the warehouse's available stocks（对应 xyl #现有量）.

c(最重要). 同一仓库同一时间段只能出货同一商品。举例来说，首先定义开始搬运时间=最晚商品调配完成时间（Spdd.zwdpwcsj）-总调配时间（queryYscb接口查询获取）
结束搬运时间=最晚商品调配完成时间（Spdd.zwdpwcsj）-运输时间（Spdd.ckData.yscb）。
假设A订单的开始搬运时间为6月6日12：00结束搬运时间为18：00；B订单的开始搬运时间为6月6日14：00，由于时间冲突，B订单无法使用A仓库.  

d. 严格按照订单顺序进行优先级分派，即保证在前面的订单必定可以满足。



**输出：**

{
        'cknm': 'WH2',  # 仓库ID
        'ddnm': '6',  # 订单ID
        'jd': 39.913818,  # 经度
        'lg': '个',  # 单位
        'qynm': '678',  # 提交订单的企业ID
        'sl': 7.0,  # 商品数量
        'spnm': 'B',  # 商品ID
        'wd': 116.363625  # 纬度
    }


## 任务

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    req = request.json  # 获取请求中的 JSON 数据

    results = []  # 创建一个空列表来保存结果

    for i in range(len(req["Spdd"])):  # 对于每个订单
        for j in range(len(req["Spdd"][i]["ckdata"])):  # 对于每个仓库
            # 在这里，我们添加一个条件判断，只有当 condition 满足时，才添加结果
            # 这个条件需要你根据实际情况来定义
            if condition:
                results.append({  # 添加一个新的结果
                    "cknm": req["Spdd"][i]["ckdata"][j]["cknm"],
                    "qynm": req["Spdd"][i]["qynm"],
                    "spnm": req["Spdd"][i]["spnm"],
                    "sl": req["Spdd"][i]["sl"],
                    "lg": req["Spdd"][i]["lg"],
                    "jd": req["Spdd"][i]["jd"],
                    "wd": req["Spdd"][i]["wd"],
                    "ddnm": req["Spdd"][i]["ddnm"]
                })

    return jsonify(results)  # 将结果作为 JSON 返回
----
请你在该算法实现前 设计一些测试样例，

