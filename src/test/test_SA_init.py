from util import *
from optimizer import *
# 本文档的目的是测试初始解的生成，即generate_initial_solution函数，测试数据在下面定义，测试结果在最后打印。

test_orders = [
    {
        'ddnm': '订单内码1',
        'qynm': '提交商品订单企业内码1',
        'spnm': '商品内码1',
        'sl': 50,
        'lg': '量纲1',
        'zwdpwcsj': '2023-10-01',
        'jd': 120,
        'wd': 30,
        'ckdata': [
            {
                'cknm': '仓库内码1',
                'xyl': 60,
                'yscb': 6.0
            },
            {
                'cknm': '仓库内码2',
                'xyl': 70,
                'yscb': 8.0
            }
        ]
    },
    {
        'ddnm': '订单内码2',
        'qynm': '提交商品订单企业内码2',
        'spnm': '商品内码2',
        'sl': 100,
        'lg': '量纲2',
        'zwdpwcsj': '2023-10-05',
        'jd': 130,
        'wd': 40,
        'ckdata': [
            {
                'cknm': '仓库内码3',
                'xyl': 200,
                'yscb': 10.0
            },
            {
                'cknm': '仓库内码4',
                'xyl': 150,
                'yscb': 12.0
            }
        ]
    }
]

# 生成初始解
initial_solution = generate_initial_solution(test_orders)

# 打印初始解
for strategy in initial_solution:
    print(strategy)

