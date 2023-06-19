from util import *


from datetime import timedelta

def resolve_time_conflict(schedule, start_time, end_time, max_attempts=1000):
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
