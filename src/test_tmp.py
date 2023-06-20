import collections
from util import *

orders = read_orders_from_file('orders_data2.json')
# strategies = order_to_strategy(orders)
# print(strategies)
# just print the ddnm, cknm, sl of strategy
# for item in strategies:
#     print(item.get("ddnm"), item.get("cknm"), item.get("sl"))


strategies=[]
def get_warehouse_capacity(cknm, spnm,zwkssj):
    """
    Get the available capacity of a specific warehouse for a specific product.

    Args:
    cknm (str): The warehouse ID.
    spnm (str): The product ID.

    Returns:
    int: The available capacity of the warehouse for the product. Returns None if the warehouse or product doesn't exist.
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
    #return a dict to implement get_ckdata_for_order(ddnm)
    ckdata_for_order={}
    sl_for_order={}
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
        ckdata_for_order[ddnm]=ckdata_list
        sl_for_order[ddnm]=total_sl
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
            # If the warehouse's capacity is greater than or equal to the total order quantity, allocate the total quantity from this warehouse. Otherwise, allocate as much as possible from this warehouse.
            sl = min(warehouse_capacity, total_sl)
            strategy_item["sl"] = sl
            total_sl -= sl

            #calculate yscb, ksbysj, jsbysj and cb
            yscb = timedelta(hours=ckdata.get("yscb"))
            jsbysj = zwdpwcsj - yscb
            ztpsj = timedelta(hours=get_total_dispatch_cost(spnm, cknm, jd, wd, sl, lg))
            ksbysj = zwdpwcsj - ztpsj

            strategy_item["xqsj"] = zwdpwcsj
            strategy_item["ksbysj"] = ksbysj
            strategy_item["jsbysj"] = jsbysj
            strategy_item["cb"] = ztpsj
            strategy_item["lg"] = lg

            strategies.append(strategy_item)

            # Break the loop if the total order quantity has been allocated.
            if total_sl <= 0:
                break

    return strategies, ckdata_for_order, sl_for_order


#print(init_strategy)

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

def neighbor(state,ckdata_for_order):
    """
    Generate a new state from the current one by changing some strategies.

    Args:
    state (list): A list of strategies, each represented as a dictionary.

    Returns:
    list: A new state obtained by changing some strategies.
    """
    # First, make a copy of the current state so we don't modify the original state.
    new_state = deepcopy(state)

    # Randomly select a strategy to change.
    strategy_to_change = random.choice(new_state)
    
    # Get the 'ckdata' for the order corresponding to this strategy.
    ckdata_list = ckdata_for_order[strategy_to_change["ddnm"]]
    
    # Randomly select a new warehouse, different from the current one.
    new_warehouse = random.choice([ckdata for ckdata in ckdata_list if ckdata.get("cknm") != strategy_to_change["cknm"]])

    # Update the strategy with the new warehouse's details.
    strategy_to_change["cknm"] = new_warehouse.get("cknm")

    # Recalculate 'ksbysj', 'jsbysj', and 'cb'.
    yscb = timedelta(hours=new_warehouse.get("yscb"))
    ztpsj = timedelta(hours=get_total_dispatch_cost(strategy_to_change["spnm"], new_warehouse.get("cknm"), strategy_to_change["jd"], strategy_to_change["wd"], strategy_to_change["sl"], strategy_to_change["lg"]))
    
    strategy_to_change["ksbysj"] = strategy_to_change["xqsj"] - ztpsj
    strategy_to_change["jsbysj"] = strategy_to_change["xqsj"] - yscb
    strategy_to_change["cb"] = ztpsj

    return new_state

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

    # Check the first constraint.
    for ddnm, strategies in strategies_by_ddnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'ddnm' is less than the 'sl' of the order, return False.
        if total_sl < sl_for_order[ddnm]:
            return False

    # Check the second constraint.
    for (cknm, spnm), strategies in strategies_by_cknm_spnm.items():
        total_sl = sum(strategy["sl"] for strategy in strategies)
        # If the sum of 'sl' for a specific 'cknm' and 'spnm' is greater than the 'xyl' of the warehouse, return False.
        if total_sl > get_warehouse_capacity(cknm, spnm, strategies[0]["xqsj"].isoformat()):
            return False

    # Check the third constraint.
    for cknm, strategies in strategies_by_cknm.items():
        # Sort the strategies by 'ksbysj'.
        strategies.sort(key=lambda strategy: strategy["ksbysj"])
        # If any two adjacent strategies have overlapping time intervals, return False.
        for i in range(len(strategies) - 1):
            if strategies[i]["jsbysj"] > strategies[i + 1]["ksbysj"]:
                return False

    # If none of the constraints is violated, the state is valid.
    return True

def acceptance_probability(old_cost, new_cost, temperature):
    # If the new cost is lower, always accept it.
    if new_cost < old_cost:
        return 1

    # If the new cost is higher, accept it with a probability that decreases as the difference between the new cost and the old cost increases, and as the temperature decreases.
    return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    # Set the initial state and temperature.
    state, ckdata_for_order, sl_for_order = initial_state(orders)
    temperature = 1.0
    cooling_rate = 0.5
    max_attempts = 1  # Set a maximum limit for attempts.

    attempts = 0  # Initialize the counter for attempts.

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

        if acceptance_probability(old_cost, new_cost, temperature) > random.random():
            state = new_state

        # Decrease the temperature.
        temperature *= 1 - cooling_rate
    if is_valid(state, sl_for_order):
        return state
    else:
        return None

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

solution=simulated_annealing()
solution = format_solution(solution)
print(solution)