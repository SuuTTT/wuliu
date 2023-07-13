## 算法设计文档


### 问题定义

#### **优化物流分配**

考虑一个物流分配场景，有 $m$ 个订单，$n$ 个仓库，和 $l$ 种货物。任务是找到一个分配方案，最大化总体满足度，同时最小化最大的运输时间。

输入数据包括：

- $X_{m \times n \times l}$: 三维矩阵，表示每种货物从每个仓库到每个订单的单位运输时间（单位：小时）。
- $Y_{m \times l}$: 矩阵，表示每个订单对每种货物的需求量。
- $Z_{n \times l}$: 矩阵，表示每个仓库每种货物的库存量。
- $O_{m}$: 矩阵，表示每个订单的优先级（无单位）。
- $W_{n}$: 矩阵，表示每个仓库的优先级（无单位）。

输出应该是：

- $A_{m \times n \times l}$: 三维矩阵，表示每种货物从每个仓库到每个订单的运输量。
- $B_{m \times n \times l}$: 三维矩阵，表示每种货物从每个仓库到每个订单的运输时间。
- $B_{m \times n \times l} = A_{m \times n \times l} \circ X_{m \times n \times l}$

#### 目标

目标是最小化以下目标函数：

\[
\text{Minimize } Z = \left( \max_{i=1}^{m} \sum_{j=1}^{n} \sum_{l=1}^{L} b_{ijl} \right)
\]

#### 约束条件

- 对于所有的 j 和 l，有 `0 <= ∑(i=1 to m) a[i][j][l] <= z[j][l]`
- 对于所有的 i 和 l，有 `0 <= ∑(j=1 to n) a[i][j][l] <= y[i][l]`
- 对于所有的 j 和 l，当库存 z[j][l] 不足以满足所有订单需求时，需要尽可能用完库存：`∑(i=1 to m) a[i][j][l] = z[j][l]`
- 对于所有的 i 和 l，我们要保证高优先级的订单尽可能得到满足：如果 `O[i] > O[k]`，那么 `∑(j=1 to n) a[i][j][l] >= ∑(j=1 to n) a[k][j][l]`，其中 k 是任意的 i 以外的订单。

---

### 解决方案

该问题可以通过构建网络流模型并求解最小成本最大流问题来解决。

1. **创建源点和汇点**：创建一个源点 S 和一个汇点 T。源点代表商品的来源，汇点代表商品的消费。

2. **创建仓库节点和订单节点**：对于每个仓库 `j` 和每种商品 `l`，我们创建一个节点 `Warehouse_j_l`。类似地，对于每个订单 `i` 和每种商品 `l`，我们创建一个节点 `Order_i_l`。

3. **连接源点和仓库节点**：对于每个 `Warehouse_j_l` 节点，我们从源点 S 到这个节点添加一条边。边的容量等于该仓库对于该种商品的库存量 `z[j][l]`。这条边的费用为0。

4. **连接仓库节点和订单节点**：对于每个仓库 `j`、每个订单 `i` 和每种商品 `l`，我们从 `Warehouse_j_l` 节点到 `Order_i_l` 节点添加一条边。边的容量为无限大（实际上，在计算时，可以设置为一个足够大的数），边的费用为该种商品从该仓库到该订单的单位运输时间 `x[i][j][l]`。

5. **连接订单节点和汇点**：对于每个 `Order_i_l` 节点，我们从这个节点到汇点 T 添加一条边。边的容量等于该订单对于该种商品的需求量 `y[i][l]`。这条边的费用为0。

最后，通过求解最小成本最大流问题，我们可以找到最优的分配方案。这个问题可以使用各种已知的最小成本最大流算法来求解，例如 Bellman-Ford 算法、Dijkstra 算法+Johnson 算法等。

注意，对于库存不足和订单优先级的问题，需要在求解最小成本最大流问题时，针对每个订单按照优先级的顺序来分配商品，优先级高的订单先分配。同时，如果一个仓库的某种商品库存不足，那么我们就从该仓库的其他商品开始分配。

最后，得到的最大流就是每种商品从每个仓库到每个订单的最优运输量，而最小成本就是最大运输时间。


### 测试代码

好的，让我们创建一个例子来测试上述代码。

假设有3个仓库（节点0、1、2），3个订单（节点3、4、5）。仓库到订单的传输时间和货物量如下：

```
Warehouse 0 -> Order 3: 10 units, 5 hours/unit
Warehouse 1 -> Order 4: 5 units, 10 hours/unit
Warehouse 2 -> Order 5: 5 units, 15 hours/unit
```

此外，仓库之间也有一些可以流动的商品：

```
Warehouse 0 -> Warehouse 1: 10 units, 1 hour/unit
Warehouse 1 -> Warehouse 2: 10 units, 1 hour/unit
```

以下是测试代码：

```cpp
int main() {
    // The nodes 0, 1, 2 are warehouses
    // The nodes 3, 4, 5 are orders
    // The nodes 6 is the source node
    // The node 7 is the sink node
    AddEdge(6, 0, 10, 0);  // Supply from the source to the warehouses
    AddEdge(6, 1, 5, 0);
    AddEdge(6, 2, 5, 0);

    AddEdge(0, 3, 10, 5);  // From warehouse to order
    AddEdge(1, 4, 5, 10);
    AddEdge(2, 5, 5, 15);

    AddEdge(0, 1, 10, 1);  // Between warehouses
    AddEdge(1, 2, 10, 1);

    AddEdge(3, 7, 10, 0);  // Demand from the orders to the sink
    AddEdge(4, 7, 5, 0);
    AddEdge(5, 7, 5, 0);

    int cost;
    int maxFlow = MinCostMaxFlow(6, 7, cost);

    cout << "The maximum flow is " << maxFlow << endl;
    cout << "The minimum cost (maximum transportation time) is " << cost << endl;

    return 0;
}
```

在这个例子中，最大流应该是20，这是因为总的商品数量是20，并且每个订单的需求总和也是20。最小成本应该是150，这是最优的货物分配策略所需要的最大运输时间。