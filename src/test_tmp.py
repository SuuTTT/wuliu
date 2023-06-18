from optimizer import *
from util import *
def test():
    orders_data = {
        "Spdd": [
            {
                "ddnm": "订单内码1",
                "qynm": "提交商品订单企业内码1",
                "spnm": "商品内码1",
                "sl": "商品数量1",
                "lg": "量纲1",
                "zwdpwcsj": "2023-06-30T00:00:00",
                "jd": 39.913818,
                "wd": 116.363625,
                "ckdata": [
                    {
                        "cknm": "仓库内码1",
                        "pfwhnm": "剖分网盒内码1",
                        "yscb": 6.0
                    },
                    {
                        "cknm": "仓库内码2",
                        "pfwhnm": "剖分网盒内码2",
                        "yscb": 6.0
                    }
                ]
            },
            # Add more orders here...
        ],
    }
    orders, warehouses = parse_data(orders_data)
    assert len(orders) == 1
    assert len(warehouses) == 2
    assert orders[0]["id"] == "订单内码1"
    assert warehouses[0]["id"] == "仓库内码1"

    schedule = {
        "start": "2023-06-29T18:00:00",
        "end": "2023-06-29T23:00:00",
    }
    assert is_schedule_conflict(schedule, orders[0])  # This should be True

    schedule = {
        "start": "2023-06-30T01:00:00",
        "end": "2023-06-30T06:00:00",
    }
    assert not is_schedule_conflict(schedule, orders[0])  # This should be False


if __name__ == "__main__":
    test()
