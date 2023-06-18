from util import *

def generate_initial_solution(orders, warehouses):
    solution = {}
    for order in orders:
        # Find a warehouse that can satisfy the order
        for warehouse_info in order["ckdata"]:
            warehouse_id = warehouse_info["cknm"]
            warehouse = warehouses[warehouse_id]
            # Check if the warehouse's inventory and schedule can satisfy the order
            if is_warehouse_available(warehouse, order):
                # Assign the warehouse to the order
                solution[order["ddnm"]] = warehouse_id
                # Update the warehouse's inventory and schedule
                update_warehouse(warehouse, order)
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
