from util import *

orders = read_orders_from_file('orders_data.json')
strategy = order_to_strategy(orders)
print(strategy)
# just print the ddnm, cknm, sl of strategy
for item in strategy:
    print(item.get("ddnm"), item.get("cknm"), item.get("sl"))

# get the xyl of all warehouse by calling get_all_warehouses_xyl
warehouses = get_all_warehouses_xyl(strategy, strategy[0].get("xqsj").isoformat())
print(warehouses)
