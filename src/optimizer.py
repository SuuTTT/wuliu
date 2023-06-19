from util import *

def generate_initial_solution(orders):
    solution = []
    for order in orders:
        # 对于每个订单，找到可以提供商品的仓库
        available_warehouses = [warehouse for warehouse in order['ckdata'] if warehouse['xyl'] >= order['sl']]
        if not available_warehouses:
            # 如果没有仓库可以提供足够的商品，跳过这个订单
            continue
        # 选择成本最小的仓库
        selected_warehouse = min(available_warehouses, key=lambda x: x['yscb'])
        # 计算搬运开始和结束时间
        total_dispatch_time = get_total_dispatch_cost(order['spnm'], selected_warehouse['cknm'], order['jd'], order['wd'], order['sl'], order['lg'])
        start_dispatch_time = order['zwdpwcsj'] - total_dispatch_time
        end_dispatch_time = order['zwdpwcsj'] - selected_warehouse['yscb']
        # 添加到解中
        solution.append({
            'cknm': selected_warehouse['cknm'],
            'qynm': order['qynm'],
            'spnm': order['spnm'],
            'xqsj': order['zwdpwcsj'],
            'ksbysj': start_dispatch_time,
            'jsbysj': end_dispatch_time,
            'cb': total_dispatch_time,
            'sl': order['sl'],
            'lg': order['lg'],
            'jd': order['jd'],
            'wd': order['wd'],
            'ddnm': order['ddnm']
        })
    return solution


def is_warehouse_available(warehouse, order):
    # Check if the warehouse's inventory is enough for the order
    if warehouse["inventory"] < order["sl"]:
        return False
    # Check if the warehouse's schedule is available for the order
    for schedule in warehouse["schedules"]:
        if is_schedule_conflict(schedule, order):
            return False
    return True

def is_schedule_conflict(schedule, order):
    # Check if the order's schedule conflicts with the warehouse's schedule
    order_start = get_order_start_time(order)
    order_end = get_order_end_time(order)
    if order_start < schedule["end"] and order_end > schedule["start"]:
        return True
    return False

def update_warehouse(warehouse, order):
    # Update the warehouse's inventory
    warehouse["inventory"] -= order["sl"]
    # Update the warehouse's schedule
    warehouse["schedules"].append({
        "start": get_order_start_time(order),
        "end": get_order_end_time(order),
        "order_id": order["ddnm"],
        "product_id": order["spnm"]
    })
