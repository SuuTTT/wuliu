from optimizer import *
# 这个文件的目的是测试初始解的生成，即generate_initial_solution函数，测试数据在下面定义，测试结果在最后打印。
# 这个测试文件与test_SA_init.py的区别在于，这个文件的测试数据中有冲突的订单，修复了resolve_conflict函数中的bug。
def test_generate_initial_solution():
    orders = [
        {
            'ckdata': [
                {'cknm': 'Warehouse1', 'xyl': 100, 'yscb': 5},
                {'cknm': 'Warehouse2', 'xyl': 100, 'yscb': 7}
            ],
            'qynm': 'Region1',
            'spnm': 'Product1',
            'zwdpwcsj': '2023-06-30',
            'sl': 10,
            'lg': 'kg',
            'jd': 31.2304,
            'wd': 121.4737,
            'ddnm': 'Order1'
        },
        {
            'ckdata': [
                {'cknm': 'Warehouse1', 'xyl': 100, 'yscb': 5},
                {'cknm': 'Warehouse2', 'xyl': 100, 'yscb': 7}
            ],
            'qynm': 'Region2',
            'spnm': 'Product2',
            'zwdpwcsj': '2023-06-30',
            'sl': 20,
            'lg': 'kg',
            'jd': 39.9042,
            'wd': 116.4074,
            'ddnm': 'Order2'
        },
        {
            'ckdata': [
                {'cknm': 'Warehouse1', 'xyl': 100, 'yscb': 5},
                {'cknm': 'Warehouse2', 'xyl': 100, 'yscb': 7}
            ],
            'qynm': 'Region3',
            'spnm': 'Product3',
            'zwdpwcsj': '2023-06-30',
            'sl': 300,
            'lg': 'kg',
            'jd': 29.4316,
            'wd': 106.9123,
            'ddnm': 'Order3'
        },
    ]

    solution = generate_initial_solution(orders)

    # 检查解的长度是否正确
    #assert len(solution) == 3
    print(solution)
    # 检查解的内容是否正确
    for sol in solution:
        #assert sol['sl'] <= 100  # 确保每个解的商品数量不超过100
        assert 'cknm' in sol  # 确保解包含了仓库名称
        assert 'ksbysj' in sol and 'jsbysj' in sol  # 确保解包含了开始和结束搬运时间

    print('All tests passed.')

test_generate_initial_solution()
