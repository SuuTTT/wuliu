## 选择订单的逻辑

```python
def neighbour(solution):
    # 生成新解，这里我们随机交换两个订单的仓库
    new_solution = copy.deepcopy(solution)
    i, j = random.sample(range(len(new_solution)), 2)
    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
    return new_solution
```
这里的配送逻辑不是这样的。
1. 没有考虑商品，仓库里有多种商品，而订单只会请求一种商品
2. 当订单及其请求商品X固定时，仓库和订单是多对一的关系，可从多个仓库给同一个订单提供X商品。

> 看起来您的需求更复杂一些，这种情况下，我们需要更详细地定义什么是一个“解”，以及如何从一个解移动到它的“邻域”。
>
> 一种可能的方式是将一个解定义为一个订单到仓库的映射，其中每个订单可以映射到多个仓库，即每个订单的商品可以从多个仓库获得。
>
> 那么，一个邻域解可以是这样产生的：随机选择一个订单，然后在它映射的仓库列表中随机添加或删除一个仓库。如果添加的仓库没有存储订单所需的商品，或者删除的仓库是订单唯一的提供者，那么这个改动就会被忽略，再随机选择一种改动，直到找到一个有效的邻域解。
>
> 例如，我们可以改写`neighbour()`函数如下：
>
> ```python
> def neighbour(solution):
>     new_solution = copy.deepcopy(solution)
>     while True:
>         order = random.choice(new_solution)  # 随机选择一个订单
>         warehouse = random.choice(warehouses)  # 随机选择一个仓库
>         if warehouse in order['warehouses']:
>             if len(order['warehouses']) > 1:  # 如果这个仓库不是唯一的提供者
>                 order['warehouses'].remove(warehouse)  # 尝试移除这个仓库
>                 break
>         elif warehouse_has_item(warehouse, order['item']):  # 如果这个仓库有存储所需商品
>             order['warehouses'].append(warehouse)  # 尝试添加这个仓库
>             break
>     return new_solution
> ```
>
> 在这段代码中，`warehouses`是全部仓库的列表，`warehouse_has_item(warehouse, item)`是一个函数，用于检查某个仓库是否存储有某种商品。
>
> 这样，我们就可以在保证每个订单都有至少一个仓库可以提供所需商品的前提下，随机改动订单到仓库的映射，从而产生邻域解。
