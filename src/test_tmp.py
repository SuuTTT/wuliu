from util import *
from optimizer import *

def test_get_neighbor():
    orders = read_orders_from_file('orders_data.json')  # 读取原始订单数据
    #print(orders)
    initial_solution = generate_initial_solution(orders)  # 使用原始订单数据生成初始解
    #print(initial_solution)
    warehouse_schedules = generate_warehouse_schedules(initial_solution)  # 根据初始解生成仓库调度时间表
    neighbor = get_neighbor(initial_solution, orders, warehouse_schedules)  # 尝试在另一个仓库进行调度
    print(neighbor)

test_get_neighbor()
