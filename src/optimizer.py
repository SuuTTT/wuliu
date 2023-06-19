from util import *
from datetime import timedelta
import random
import argparse
def resolve_time_conflict(schedule, start_time, end_time, max_attempts=120):
    """尝试移动调度时间以解决时间冲突"""
    # 尝试移动的时间间隔
    interval = timedelta(hours=1)

    attempts = 0

    # 向前移动调度时间，直到没有冲突
    new_start_time = start_time
    new_end_time = end_time
    while any(new_start_time <= end and new_end_time >= start for start, end in schedule) and attempts < max_attempts:
        new_start_time -= interval
        new_end_time -= interval
        attempts += 1

    if attempts < max_attempts:
        # 如果向前移动解决了冲突，则返回新的调度时间
        return new_start_time, new_end_time

    # 如果向前移动没能解决冲突，尝试向后移动调度时间
    attempts = 0
    new_start_time = start_time
    new_end_time = end_time
    while any(new_start_time <= end and new_end_time >= start for start, end in schedule) and attempts < max_attempts:
        new_start_time += interval
        new_end_time += interval
        attempts += 1

    if attempts < max_attempts:
        # 如果向后移动解决了冲突，返回新的调度时间
        return new_start_time, new_end_time

    # 如果仍然有冲突，返回None
    return None, None

def generate_initial_solution(orders):
    solution = []
    # 创建一个字典，为每个仓库建立一个调度表
    warehouse_schedules = {}

    for order in orders:
        remaining_quantity = order['sl']  # 该订单的剩余需求量

        # 获取可以为该订单供货的所有仓库，注意现在我们不再需要满足仓库的库存量大于订单需求量这一条件
        available_warehouses = [warehouse for warehouse in order['ckdata'] if warehouse['xyl'] > 0]

        # 对可用仓库按照成本进行排序
        available_warehouses.sort(key=lambda x: x['yscb'])

        for warehouse in available_warehouses:
            # 计算从这个仓库分配的商品数量，不能超过仓库的库存量，也不能超过订单的剩余需求量
            dispatch_quantity = min(warehouse['xyl'], remaining_quantity)

            total_dispatch_cost = get_total_dispatch_cost(order['spnm'], warehouse['cknm'], order['jd'], order['wd'], dispatch_quantity, order['lg'])
            total_dispatch_time = total_dispatch_cost['data'] if total_dispatch_cost else None

            zwdpwcsj = datetime.strptime(order['zwdpwcsj'], '%Y-%m-%d')
            start_dispatch_time = zwdpwcsj - timedelta(hours=total_dispatch_time)
            end_dispatch_time = zwdpwcsj - timedelta(hours=warehouse['yscb'])

            # 获取这个仓库的调度表
            schedule = warehouse_schedules.get(warehouse['cknm'], [])

            # 检查是否可以在这个时间段调度商品
            while any(start_dispatch_time <= end_time and end_dispatch_time >= start_time for start_time, end_time in schedule):
                # 如果有冲突，尝试解决冲突
                start_dispatch_time, end_dispatch_time = resolve_time_conflict(schedule, start_dispatch_time, end_dispatch_time)
                if start_dispatch_time is None:
                    # 如果无法解决冲突，跳过这个仓库
                    break

            if start_dispatch_time is None:
                continue

            # 如果可以在这个时间段调度商品，或解决了冲突，那么更新这个仓库的调度表
            schedule.append((start_dispatch_time, end_dispatch_time))
            warehouse_schedules[warehouse['cknm']] = schedule

            solution.append({
                'cknm': warehouse['cknm'],
                'qynm': order['qynm'],
                'spnm': order['spnm'],
                'xqsj': order['zwdpwcsj'],
                'ksbysj': start_dispatch_time,
                'jsbysj': end_dispatch_time,
                'cb': total_dispatch_time,
                'sl': dispatch_quantity,  # 这个调度策略的商品数量是从这个仓库分配的商品数量
                'lg': order['lg'],
                'jd': order['jd'],
                'wd': order['wd'],
                'ddnm': order['ddnm']
            })

            # 更新订单的剩余需求量
            remaining_quantity -= dispatch_quantity

            # 如果订单的全部需求量已经被满足，那么就跳出循环，开始处理下一个订单
            if remaining_quantity <= 0:
                break

    return solution


def generate_warehouse_schedules(solution):
    """根据解生成仓库调度时间表"""
    warehouse_schedules = {}
    for dispatch in solution:
        # 如果仓库还没有调度时间表，创建一个新的空列表
        if dispatch['cknm'] not in warehouse_schedules:
            warehouse_schedules[dispatch['cknm']] = []

        # 添加新的调度时间
        warehouse_schedules[dispatch['cknm']].append((dispatch['ksbysj'], dispatch['jsbysj']))

    return warehouse_schedules

def get_neighbor(solution, orders, warehouse_schedules):
    """生成邻域解"""
    # 随机选择一个订单
    order_index = random.randint(0, len(orders) - 1)
    order = orders[order_index]

    # 随机选择一个新的仓库
    available_warehouses = order['ckdata']
    warehouse_index = random.randint(0, len(available_warehouses) - 1)
    warehouse = available_warehouses[warehouse_index]

    # 为新的仓库分配尽可能多的商品
    dispatch_quantity = min(warehouse['xyl'], order['sl'])

    # 计算新的调度时间
    total_dispatch_cost = get_total_dispatch_cost(order['spnm'], warehouse['cknm'], order['jd'], order['wd'], dispatch_quantity, order['lg'])
    total_dispatch_time = total_dispatch_cost['data'] if total_dispatch_cost else None
    zwdpwcsj = datetime.strptime(order['zwdpwcsj'], '%Y-%m-%d')
    start_dispatch_time = zwdpwcsj - timedelta(hours=total_dispatch_time)
    end_dispatch_time = zwdpwcsj - timedelta(hours=warehouse['yscb'])

    # 解决可能的时间冲突
    schedule = warehouse_schedules.get(warehouse['cknm'], [])
    start_dispatch_time, end_dispatch_time = resolve_time_conflict(schedule, start_dispatch_time, end_dispatch_time)
    if start_dispatch_time is None:
        # 如果无法解决时间冲突，那么这个邻居就无效，返回原解
        return solution

    # 创建新的解，只更改选定的订单
    new_solution = solution.copy()
    new_solution[order_index] = {
        'cknm': warehouse['cknm'],
        'qynm': order['qynm'],
        'spnm': order['spnm'],
        'xqsj': order['zwdpwcsj'],
        'ksbysj': start_dispatch_time,
        'jsbysj': end_dispatch_time,
        'cb': total_dispatch_time,
        'sl': dispatch_quantity,
        'lg': order['lg'],
        'jd': order['jd'],
        'wd': order['wd'],
        'ddnm': order['ddnm']
    }

    return new_solution

def cost_function(solution):
    """Calculate the total cost of a solution."""
    total_cost = 0
    for dispatch in solution:
        # Add the dispatch cost
        total_cost += dispatch['cb']

        # Add a penalty if an order cannot be fulfilled
        # This is just a placeholder, replace with your actual constraints
        #if dispatch['sl'] < 0:
        #    total_cost += 10000  # Adjust the penalty value as needed

    return total_cost



def simulated_annealing(initial_solution, orders, warehouse_schedules, cost_function, T_initial, T_final, alpha, max_iter):
    """模拟退火算法主函数"""
    current_solution = initial_solution
    current_cost = cost_function(current_solution)
    T = T_initial

    while T > T_final:
        for _ in range(max_iter):
            new_solution = get_neighbor(current_solution, orders, warehouse_schedules)
            new_cost = cost_function(new_solution)
            cost_diff = new_cost - current_cost
            if cost_diff < 0 or random.random() < math.exp(-cost_diff / T):
                current_solution = new_solution
                current_cost = new_cost

        T *= alpha

    return current_solution


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    # 假设我们有以下订单和仓库
    orders = read_orders_from_file('orders_data.json')

    # 生成初始解
    initial_solution = generate_initial_solution(orders)

    # 生成仓库调度时间表
    warehouse_schedules = generate_warehouse_schedules(initial_solution)

    # Select parameters for regular or test run
    if args.test:  # You need to define this variable somewhere
        params = config['Test']
    else:
        params = config['SimulatedAnnealing']

    # 模拟退火算法参数
    T_initial = int(params['T_initial'])
    T_final = int(params['T_final'])
    alpha = float(params['alpha'])
    max_iter = int(params['max_iter'])


    # 执行模拟退火算法
    final_solution = simulated_annealing(initial_solution, orders, warehouse_schedules, cost_function, T_initial, T_final, alpha, max_iter)

    print(final_solution)

if __name__ == "__main__":
    main()
