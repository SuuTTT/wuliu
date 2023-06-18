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
