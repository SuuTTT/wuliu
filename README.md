# README

## 项目简介(for 项目经理)
这是一个仓储物流优化项目，旨在利用优化算法来解决复杂的物流分配问题。给定一系列的订单需求、仓库存货、以及物流运输时间，我们的目标是找到一个最优的分配计划，以使得满足订单需求的同时，最大化总体满意度并最小化最大的运输时间。

项目使用Python语言进行开发，依赖于numpy库进行矩阵计算。

## 项目结构(for 开发人员)

### 主目录:
- `README.md`: 项目的基本介绍和使用指南。
- `requirement.txt`: Python环境依赖文件。
- `doc`: 文档目录，包含项目的设计、需求、测试等文档。
- `src`: 源代码目录。

### doc目录:
- `Software_Architecture_Documentmd`: 软件架构文档。
- `bug.md`: 记录项目过程中出现的bug。
- `figure`: 项目的各种图片资料。
- `ppt`: 项目需求和设计的演示文稿。
- `prompt`: 各类提示信息和问题记录。
- `requirement.md`: 项目需求文档。
- `test.md`: 测试文档。
- `todo`: 待完成的任务记录。
- `version.md`: 项目的版本信息。

### src目录:
- `__pycache__`: Python的缓存文件目录。
- `data copy.json`: 数据备份。
- `data.json`: 数据文件。
- `optimizer.py`: 优化算法的实现文件。是本项目的核心算法
- `test`: 测试文件目录。
- `test_tmp.py`: 临时的测试文件。
- `util.py`: 包含一些实用的函数，如从json文件中加载数据并转换为矩阵的函数。

---

## 待实现函数(for 开发人员)
### optimizer.py:
该文件是项目的核心，其中定义了一个名为 `logistics_distribution` 的函数，该函数的目标是根据输入的矩阵A1，A2，A3，W1和W2（分别表示单位运输时间、各订单的商品需求、各仓库的商品存货以及订单和仓库的优先级），输出一个满足需求的分配计划，以最大化总体满意度并最小化最大的运输时间。

```python
def logistics_distribution(A1, A2, A3, W1, W2):
    """
    This function takes in five matrices A1, A2, A3, W1, W2 which represent 
    different aspects of a logistics problem. The function should output a 
    distribution plan to maximize overall satisfaction and minimize maximum 
    transportation time.
    
    Input:
    A1: A 3D numpy array of shape (m, n, k) representing the unit transportation time
    A2: A 2D numpy array of shape (m, k) representing the demand for each type of good for each order
    A3: A 2D numpy array of shape (n, k

) representing the stock of each type of good in each warehouse
    W1: A 1D numpy array of length m representing the priority of each order
    W2: A 1D numpy array of length n representing the priority of each warehouse
    
    Output:
    A distribution plan that maximizes overall satisfaction and minimizes maximum transportation time.
    """
    # Start your code here
    pass
```

该函数目前处于待实现的状态，需要开发人员根据实际的业务需求和优化策略完成具体的实现。


## 环境配置(for 运维人员)
首先，你需要确保你有以下文件：

- Miniconda 的安装包：`Miniconda3-latest-Linux-x86_64.sh`
- 打包好的 conda 环境：`wuliu.zip`
- 项目源代码：`wuliu-master.zip`

然后，按照以下步骤操作：

1. 将光盘中的 `Miniconda3-latest-Linux-x86_64.sh`、`wuliu.zip` 和 `wuliu-master.zip` 文件复制到服务器的一个目录中，例如 `/home/user/`。

2. 打开一个终端，然后运行以下命令来安装 Miniconda：

    ```bash
    chmod +x /home/user/Miniconda3-latest-Linux-x86_64.sh
    /home/user/Miniconda3-latest-Linux-x86_64.sh
    ```

    在安装过程中，你会被提示接受许可协议并选择安装位置。默认情况下，Miniconda 会安装在你的主文件夹中。

3. 安装完成后，关闭并重新打开你的终端，或者运行以下命令来更新你的 shell：

    ```bash
    source ~/.bashrc
    ```

4. 解压你的 `wuliu.zip` 文件到 conda 的环境文件夹下：

    ```bash
    unzip /home/user/wuliu.zip -d ~/miniconda3/envs/
    ```

5. 激活 `wuliu` 环境：

    ```bash
    conda activate wuliu
    ```

现在，你应该可以在你的离线计算机上使用你的 `wuliu` 环境，其中包含了所有你需要的 Python 库。

下一步，解压并使用你的项目源代码：

6. 解压项目源代码：

    ```bash
    unzip /home/user/wuliu-master.zip -d /home/user/
    ```

7. 导航到你的项目源代码的文件夹：

    ```bash
    cd /home/user/wuliu-master
    ```

现在，你应该可以在你的 `wuliu` 环境中运行你的项目源代码。如果你的项目中有 `main.py` 文件，你可以通过运行 `python main.py` 来启动你的项目。

---
:warning: **DEPRECATED**: The following information is no longer up-to-date or has been superseded by other information. It is kept here for reference only. we will update this section after the project is completed in 07/05.

~~~
## 运行项目(for 开发人员&运维人员)

1. 激活 `wuliu` 环境：

    ```bash
    conda activate wuliu
    ```
2. 导航到你的项目源代码的文件夹：

    ```bash
    cd /home/user/wuliu-master
    ```
3. 运行 `api.py` 文件, 该文件会启动一个本地服务器：

    ```bash
    python api.py
    ```
## 测试项目(for 测试人员)

1. 首先，运行 `api_mock.py` 来启模拟的本地服务器：

   ```bash
   python api_mock.py
   ```

2. 然后，您有两个并列的选项：
   
   a) 运行 `api_test.py` 来测试模拟的API：

   ```bash
   python api_test.py
   ```

   b) 或者运行 `optimizer.py` 来进行优化操作，这是更推荐的测试方法：

   ```bash
   python optimizer.py
   ```

当您运行 `optimizer.py` 时，应当会看到一个类似于下面的输出，显示了各个仓库的商品编码、需求量、搬运时间以及成本的优化结果.
note that you can change debug_output(orders, solution, language='zh') to debug_output(orders, solution, language='en') to get the output in English.

```bash
输出：
订单  需求量
    1          5
    6         14

仓库  时间段
WH1  [('06-28T17:00:00', '06-28T22:00:00'), ('06-29T14:01:00', '06-29T22:01:00')]
WH2  [('06-29T16:01:00', '06-29T23:01:00')]

仓库  商品编码  需求量  开始搬运时间  结束搬运时间  成本
WH1           AUX          5  06-28T17:00:00  06-28T22:00:00    7.0
WH1             B        8.0  06-29T14:01:00  06-29T22:01:00   10.0
WH2             B        6.0  06-29T16:01:00  06-29T23:01:00    8.0

仓库        商品编码          需求量         开始搬运时间                结束搬运时间                成本        
WH1       AUX                    5  06-28T17:00:00  06-28T22:00:00        7.00
WH1       B                    8.0  06-29T14:01:00  06-29T22:01:00       10.00
WH2       B                    6.0  06-29T16:01:00  06-29T23:01:00        8.00
```  
~~~