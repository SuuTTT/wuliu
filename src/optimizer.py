import argparse
import collections
import os
from util import *


# strategies = order_to_strategy(orders)
# print(strategies)
# just print the ddnm, cknm, sl of strategy
# for item in strategies:
#     print(item.get("ddnm"), item.get("cknm"), item.get("sl"))

def conflict_exists(existing_strategies, new_strategy):
    for strategy in existing_strategies:
        if not(strategy["ksbysj"] > new_strategy["jsbysj"] or
               strategy["jsbysj"] < new_strategy["ksbysj"]):
            return True
    return False


def get_warehouse_capacity(cknm, spnm,zwkssj):
    """
    Get the available capacity of a specific warehouse for a specific product.

    Args:
    cknm (str): The warehouse ID.
    spnm (str): The product ID.
    zwkssj (str): The start time of the warehouse. not datetime type.

    Returns:
    int: The available capacity of the warehouse list for the product. Returns None if the warehouse or product doesn't exist.
    """
    # Use the current date/time as the warehouse start time.
    
    
    # Get the warehouse inventory.
    warehouse_inventory = get_warehouse_inventory(spnm, zwkssj)
    
    if warehouse_inventory is not None and cknm in warehouse_inventory:
        return warehouse_inventory[cknm]
    else:
        return None


def initial_state(orders):
    strategies = []
    ckdata_for_order = {}
    sl_for_order = {}
    strategies_by_cknm = collections.defaultdict(list)

    for item in orders['Spdd']:
        ddnm = item.get("ddnm")
        qynm = item.get("qynm")
        spnm = item.get("spnm")
        total_sl = item.get("sl")
        lg = item.get("lg")
        jd = item.get("jd")
        wd = item.get("wd")
        zwdpwcsj = parse_date(item.get("zwdpwcsj"))

        ckdata_list = item.get("ckdata", [])
        ckdata_for_order[ddnm] = ckdata_list
        sl_for_order[ddnm] = total_sl

        for ckdata in ckdata_list:
            strategy_item = {}
            strategy_item["ddnm"] = ddnm
            strategy_item["qynm"] = qynm
            strategy_item["spnm"] = spnm

            cknm = ckdata.get("cknm")
            strategy_item["cknm"] = cknm
            strategy_item["jd"] = jd
            strategy_item["wd"] = wd

            warehouse_capacity = get_warehouse_capacity(cknm, spnm, item.get("zwdpwcsj"))

            # If the warehouse's capacity is less than the total order quantity, allocate as much as possible from this warehouse.
            sl = min(warehouse_capacity, total_sl)
            strategy_item["sl"] = sl
            total_sl -= sl

            # calculate yscb, ksbysj, jsbysj and cb
            yscb = timedelta(hours=ckdata.get("yscb"))
            jsbysj = zwdpwcsj - yscb
            ztpsj = timedelta(hours=get_total_dispatch_cost(spnm, cknm, jd, wd, sl, lg))
            ksbysj = zwdpwcsj - ztpsj

            strategy_item["xqsj"] = zwdpwcsj
            strategy_item["ksbysj"] = ksbysj
            strategy_item["jsbysj"] = jsbysj
            strategy_item["cb"] = ztpsj
            strategy_item["lg"] = lg

            # Check for time conflicts with existing strategies for this warehouse.
            if not conflict_exists(strategies_by_cknm[cknm], strategy_item):
                strategies_by_cknm[cknm].append(strategy_item)
                strategies.append(strategy_item)

            # Break the loop if the total order quantity has been allocated.
            if total_sl <= 0:
                break

    return strategies, ckdata_for_order, sl_for_order

def cost(state):
    """
    Calculate the total cost 'cb' for all strategies in the state.

    Args:
    state (list): A list of strategies, each represented as a dictionary.

    Returns:
    float: The total cost of all strategies in the state.
    """
    return sum(strategy['cb'].total_seconds()/3600 for strategy in state)


from copy import deepcopy



def neighbor(state, ckdata_for_order):
    # First, make a copy of the current state so we don't modify the original state.
    new_state = deepcopy(state)

    # Randomly select a strategy to change.
    strategy_to_change = random.choice(new_state)

    # Get the 'ckdata' for the order corresponding to this strategy.
    ckdata_list = ckdata_for_order[strategy_to_change["ddnm"]]

    # Get the warehouse stock for the current solution
    all_warehouses_xyl = get_all_warehouses_xyl(new_state, strategy_to_change["xqsj"])

    # Randomly select a new warehouse, different from the current one.
    new_warehouse = None
    for _ in range(10):  # try 10 times
        potential_warehouse = random.choice([ckdata for ckdata in ckdata_list 
                                             if ckdata.get("cknm") !=
                                               strategy_to_change["cknm"]])
        # Check the stock for the specific product in the warehouse
        if all_warehouses_xyl.get(potential_warehouse["cknm"], 
                                  {}).get(strategy_to_change["spnm"],
                                           0) >= strategy_to_change["sl"]:
            potential_strategy = strategy_to_change.copy()
            potential_strategy["cknm"] = potential_warehouse.get("cknm")
            # If there's no time conflict, use this warehouse
            if not conflict_exists([strategy for strategy in new_state if strategy["cknm"]
                                     == potential_strategy["cknm"]], potential_strategy):
                new_warehouse = potential_warehouse
                break

    if new_warehouse is None:  # if no suitable warehouse is found, return the current state
        return state

    # Update the strategy with the new warehouse's details.
    strategy_to_change["cknm"] = new_warehouse.get("cknm")

    # Recalculate 'ksbysj', 'jsbysj', and 'cb'.
    yscb = timedelta(hours=new_warehouse.get("yscb"))
    ztpsj = timedelta(hours=get_total_dispatch_cost(
        strategy_to_change["spnm"], new_warehouse.get("cknm"),
        strategy_to_change["jd"], strategy_to_change["wd"], strategy_to_change["sl"], 
        strategy_to_change["lg"]))

    strategy_to_change["ksbysj"] = strategy_to_change["xqsj"] - ztpsj
    strategy_to_change["jsbysj"] = strategy_to_change["xqsj"] - yscb
    strategy_to_change["cb"] = ztpsj

    return new_state

def acceptance_probability(old_cost, new_cost, temperature):
    # If the new cost is lower, always accept it.
    if new_cost < old_cost:
        return 1

    # If the new cost is higher, accept it with a probability that decreases as the difference between the new cost and the old cost increases, and as the temperature decreases.
    return math.exp((old_cost - new_cost) / temperature)

def is_valid(state,sl_for_order):
    """
    Check the validity of a state.

    Args:
    state (list): A list of strategies, each represented as a dictionary.

    Returns:
    bool: True if the state is valid, False otherwise.
    """
    # Group the strategies by 'ddnm', 'cknm' and 'spnm'.
    strategies_by_ddnm = collections.defaultdict(list)
    strategies_by_cknm_spnm = collections.defaultdict(list)
    strategies_by_cknm = collections.defaultdict(list)
    
    for strategy in state:
        strategies_by_ddnm[strategy["ddnm"]].append(strategy)
        strategies_by_cknm_spnm[(strategy["cknm"], strategy["spnm"])].append(strategy)
        strategies_by_cknm[strategy["cknm"]].append(strategy)

    # Check the first constraint. 满足所有订单
    for ddnm, strategies in strategies_by_ddnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'ddnm' is less than the 'sl' of the order, return False.
        if total_sl < sl_for_order[ddnm]:
            return False

    # Check the second constraint. 库存约束
    for (cknm, spnm), strategies in strategies_by_cknm_spnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'cknm' and 'spnm' is greater than the 'xyl' of the warehouse, return False.
        if total_sl > get_warehouse_capacity(cknm, spnm, strategies[0]["xqsj"].isoformat()):
            return False

    # Check the third constraint. 出库的时间约束
    for cknm, strategies in strategies_by_cknm.items():
        # Sort the strategies by 'ksbysj'.
        strategies.sort(key=lambda strategy: strategy["ksbysj"])
        # If any two adjacent strategies have overlapping time intervals, return False.
        for i in range(len(strategies) - 1):
            if strategies[i]["jsbysj"] > strategies[i + 1]["ksbysj"]:
                return False

    # If none of the constraints is violated, the state is valid.
    return True


def simulated_annealing(orders):
    # Set the initial state and temperature.
    state, ckdata_for_order, sl_for_order = initial_state(orders)
    temperature = 1.0
    cooling_rate = 0.1
    max_attempts = 100  # Set a maximum limit for attempts.

    attempts = 0  # Initialize the counter for attempts.
    
    best_state = state
    best_cost = cost(state)

    while temperature > 0.01:
        new_state = neighbor(state, ckdata_for_order)

        # Check if the new state is valid.
        if not is_valid(new_state, sl_for_order):
            attempts += 1  # Increment the counter.
            if attempts >= max_attempts:  # If the maximum limit is reached, break the loop.
                break
            continue

        old_cost = cost(state)
        new_cost = cost(new_state)

        if new_cost < best_cost:  # Store the new state if it has a lower cost.
            best_state = new_state
            best_cost = new_cost

        if acceptance_probability(old_cost, new_cost, temperature) > random.random():
            state = new_state

        # Decrease the temperature.
        temperature *= 1 - cooling_rate

    if is_valid(best_state, sl_for_order):
        return best_state,sl_for_order
    else:
        return best_state,sl_for_order  # If no valid state was found, return the state with the smallest cost.

### below are debug functions ###
#############################################################################################################
#############################################################################################################
def format_solution(solution):
    formatted_solution = []
    for strategy in solution:
        formatted_strategy = strategy.copy()
        formatted_strategy['xqsj'] = formatted_strategy['xqsj'].strftime("%Y-%m-%dT%H:%M:%S")
        formatted_strategy['ksbysj'] = formatted_strategy['ksbysj'].strftime("%Y-%m-%dT%H:%M:%S")
        formatted_strategy['jsbysj'] = formatted_strategy['jsbysj'].strftime("%Y-%m-%dT%H:%M:%S")
        formatted_strategy['cb'] = formatted_strategy['cb'].total_seconds() / 3600
        formatted_solution.append(formatted_strategy)
    return formatted_solution

def check_constraints(state, sl_for_order, language='en'):
    # Set up language-specific labels.
    if language == 'en':
        violated_label = "Violated Constraints"
        order_label = "Order"
        insufficient_label = "Insufficient quantity"
        warehouse_label = "Warehouse"
        product_code_label = "Product Code"
        exceeding_label = "Exceeding warehouse capacity"
        overlap_label = "Overlapping time intervals"
    else:  # Default to Chinese.
        violated_label = "违反的约束"
        order_label = "订单"
        insufficient_label = "需求量不足"
        warehouse_label = "仓库"
        product_code_label = "商品编码"
        exceeding_label = "超过仓库容量"
        overlap_label = "时间段重叠"

    violations = []

    # Group the strategies by 'ddnm', 'cknm' and 'spnm'.
    strategies_by_ddnm = collections.defaultdict(list)
    strategies_by_cknm_spnm = collections.defaultdict(list)
    strategies_by_cknm = collections.defaultdict(list)
    
    for strategy in state:
        strategies_by_ddnm[strategy["ddnm"]].append(strategy)
        strategies_by_cknm_spnm[(strategy["cknm"], strategy["spnm"])].append(strategy)
        strategies_by_cknm[strategy["cknm"]].append(strategy)

    # Check the first constraint.
    for ddnm, strategies in strategies_by_ddnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'ddnm' is less than the 'sl' of the order, add a violation.
        if total_sl < sl_for_order[ddnm]:
            violations.append(f"{order_label} {ddnm}: {insufficient_label}")

    # Check the second constraint.
    for (cknm, spnm), strategies in strategies_by_cknm_spnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'cknm' and 'spnm' is greater than the 'xyl' of the warehouse, add a violation.
        if total_sl > get_warehouse_capacity(cknm, spnm, strategies[0]["xqsj"]):
            violations.append(f"{warehouse_label} {cknm}, {product_code_label} {spnm}: {exceeding_label}")

    # Check the third constraint.
    for cknm, strategies in strategies_by_cknm.items():
        # Sort the strategies by 'ksbysj'.
        strategies.sort(key=lambda strategy: strategy["ksbysj"])
        # If any two adjacent strategies have overlapping time intervals, add a violation.
        for i in range(len(strategies) - 1):
            if strategies[i]["jsbysj"] > strategies[i + 1]["ksbysj"]:
                violations.append(f"{warehouse_label} {cknm}: {overlap_label}")

    # Return the violations as a string.
    if violations:
        return f"{violated_label}:\n" + "\n".join(violations)
    else:
        return "Test suceeded, No other constraints violated."





def debug_output(orders, solution, sl_for_order, language='en'):
    # Set up language-specific labels.
    if language == 'en':
        order_label = "Order"
        quantity_label = "Quantity"
        warehouse_label = "Warehouse"
        intervals_label = "Intervals"
        product_code_label = "Product Code"
        start_time_label = "Start Moving Time"
        end_time_label = "End Moving Time"
        cost_label = "Cost"
        inventory_label = "Inventory"
        unserviced_label = "Unserviced Orders"
    else:  # Default to Chinese.
        order_label = "订单"
        quantity_label = "需求量"
        warehouse_label = "仓库"
        intervals_label = "时间段"
        product_code_label = "商品编码"
        start_time_label = "开始搬运时间"
        end_time_label = "结束搬运时间"
        cost_label = "成本"
        inventory_label = "库存"
        unserviced_label = "未完成的订单（出库时间冲突）"
    
    # Get the order demands and store them in a set.
    print(f"{order_label:6}  {quantity_label:10}")
    order_codes = set()
    for order in orders['Spdd']:
        order_code = order['ddnm']
        order_codes.add(order_code)
        print(f"{order_code:6}  {order['sl']:10}")

    # Get the warehouse usage intervals and inventory.
    zwkssj=orders['Spdd'][0]['zwdpwcsj']
    all_warehouses_xyl = get_all_warehouses_xyl(solution, zwkssj)

    print(f"\n{warehouse_label:8}  {intervals_label}  {inventory_label}")
    warehouse_intervals = collections.defaultdict(list)

    for strategy in solution:
        warehouse_intervals[strategy['cknm']].append((strategy['ksbysj'][5:], strategy['jsbysj'][5:]))  # Skip the year in the timestamps.

    for warehouse, intervals in warehouse_intervals.items():
        intervals.sort(key=lambda x: x[0])  # Sort the intervals by start time.
        intervals_str = ', '.join([f"({start}, {end})" for start, end in intervals])
        # Fetch the inventory for each spnm in the warehouse
        warehouse_inventory = all_warehouses_xyl.get(warehouse, {})
        xyl_str = ', '.join([f"{spnm}: {xyl}" for spnm, xyl in warehouse_inventory.items()])
        print(f"{warehouse:8}  {intervals_str}  {xyl_str}")

    # Get the solution details.
    print(
        f"\n{warehouse_label:8} {order_label:6}"
        f" {product_code_label:12} {quantity_label:10}"
        f" {start_time_label:20} {end_time_label:20}"
        f" {cost_label:10}"
    )
    for strategy in solution:
        print(
            f"{strategy['cknm']:8} {strategy['ddnm']:6}"
            f" {strategy['spnm']:12} {strategy['sl']:10}"
            f" {strategy['ksbysj'][5:]} {strategy['jsbysj'][5:]}"
            f" {strategy['cb']:10.2f}"
        )

    # Also collect the order codes from the solution.
    solution_order_codes = {strategy['ddnm'] for strategy in solution}
    unserviced_orders = order_codes - solution_order_codes
    if unserviced_orders:
        print("\n" + unserviced_label + ":")
        for order_code in unserviced_orders:
            print(order_code)

    print(check_constraints(solution, sl_for_order, language))


def main(file_index):
    file_path = os.path.join('./test/data/', f'orders_data_{file_index}.json')
    orders = read_orders_from_file(file_path)
    solution, sl_for_order = simulated_annealing(orders)
    solution = format_solution(solution)
    debug_output(orders, solution, sl_for_order, language='zh')  # Set the language as 'zh' for Chinese or 'en' for English.


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the optimizer with specified file index.')
    parser.add_argument('-i', type=int, required=True, help='The index of the data file to use')
    args = parser.parse_args()
    main(args.i)