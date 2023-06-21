## 环境配置
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

## 运行项目

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
## 测试项目

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