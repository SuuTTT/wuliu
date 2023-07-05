import numpy as np
import pygad
import json

def logistics_distribution(X, Y, Z, O, W, order_list, warehouse_list, goods_list, goods_dict):
    """
    This function takes in five matrices X, Y, Z, O, W which represent 
    different aspects of a logistics problem. The function should output a 
    distribution plan to maximize overall satisfaction and minimize maximum 
    transportation time.
    
    Input:
    X: A 3D numpy array of shape (m, n, k) representing the unit transportation time
    Y: A 2D numpy array of shape (m, k) representing the demand for each type of good for each order
    Z: A 2D numpy array of shape (n, k) representing the stock of each type of good in each warehouse
    O: A 1D numpy array of length m representing the priority of each order
    W: A 1D numpy array of length n representing the priority of each warehouse
    
    Output:
    A distribution plan that maximizes overall satisfaction and minimizes maximum transportation time.

    """

    A_greed = greedy_solution(X,Y,Z,O,W)

    # 设置满足度和运输时间的权重
    alpha = 0.5
    beta = 0.5

    # Normalize X and store the min and max for later denormalization
    X_min, X_max = X.min(), X.max()
    X_norm = (X - X_min) / (X_max - X_min + 1e-10)

    # 初始化解向量 A
    A = np.zeros_like(X, dtype=int)
    
    # 处理订单需求数据
    Y_copy = Y.copy()
    Y_copy[np.where(Y==0)] = np.inf
    
    # 定义约束的判断函数
    def constraints_sati(A):
        A.resize(X.shape)
        if (np.sum(A, axis=0) < 0).any():
            return False
        elif ((np.sum(A, axis=0) - Z) > 0).any():
            return False
        elif (np.sum(A, axis=1) < 0).any():
            return False
        elif ((np.sum(A, axis=1) - Y) > 0).any():
            return False
        elif np.sum(A) - np.sum(Y) < 0:
            return False
        else:
            return True
            # Y = X * A1
            # fitness_sati = alpha * np.sum(O * np.sum(np.sum(X * W[np.newaxis,:,np.newaxis], axis=1) / A2_copy, axis=-1), axis=0)
            # fitness_time = beta * np.max(np.sum(Y, axis=(1,2)))
            # fitness = fitness_sati - fitness_time
            # return fitness
    # 定义带有惩罚项的满足度计算函数
    def fitness_func_penalty(ga_instance, A, A_idx):
        # A is solution
        # setting constraints
        A.resize(X.shape)
        penalty = 0

        # adjust the penalties based on your requirements
        if (np.sum(A, axis=0) < 0).any():
            penalty += np.sum(np.abs(np.sum(A, axis=0)[np.sum(A, axis=0) < 0]))
        if ((np.sum(A, axis=0) - Z) > 0).any():
            penalty += np.sum(np.abs(np.sum(A, axis=0) - Z)[(np.sum(A, axis=0) - Z) > 0])
        if (np.sum(A, axis=1) < 0).any():
            penalty += np.sum(np.abs(np.sum(A, axis=1)[np.sum(A, axis=1) < 0]))
        if ((np.sum(A, axis=1) - Y) > 0).any():
            penalty += np.sum(np.abs(np.sum(A, axis=1) - Y)[(np.sum(A, axis=1) - Y) > 0])
        if np.sum(A) - np.sum(Y) < 0:
            penalty += (np.sum(Y) - np.sum(A))

        B = A * X_norm
        B_norm = B / (np.minimum(np.max(Y), np.max(Z)) + 1e-10)
        # B_norm = (B - B.min())/(B.max() - B.min() + 1e-10)
        fitness_sati = alpha * np.sum(O * np.sum(np.sum(A * W[np.newaxis, :, np.newaxis], axis=1) / Y_copy, axis=-1),
                                      axis=0) / (Y.shape[0]*Y.shape[1])
        fitness_time = beta * np.max(np.sum(B_norm, axis=(1, 2)) / (Z.shape[0]*Z.shape[1]))
        fitness = fitness_sati - fitness_time - penalty

        return fitness

    print("fitness of greedy solution is: {}".format(fitness_func_penalty(None, A_greed, None)))

    # 设置使用带有惩罚项的满足度计算函数
    fitness_function = fitness_func_penalty

    # 设置遗传算法的参数
    num_generations = 5000         # 迭代次数
    num_parents_mating = 8         # 交配的父母数量
    sol_per_pop = 16                # 种群中的解的数量
    num_genes = A.shape[0]*A.shape[1]*A.shape[2]  # 每个解中的基因数量
    # init_range_low = 0            # 初始化解的下限
    # init_range_high = 5            # 初始化解的上限
    parent_selection_type = "sss"  # 选择父母的类型
    keep_parents = 2              # 保留父母的数量
    crossover_type = "single_point" # 交叉类型
    mutation_type = "random"       # 变异类型
    mutation_percent_genes = 30    # 变异基因的百分比

    # 计算基因空间的上限
    gene_space_high = np.minimum(Y[:,np.newaxis,:], Z[np.newaxis,:,:]).flatten().tolist()
    gene_space = [np.arange(0, int(high+1)) for high in gene_space_high]
    # 设置初始化种群，其中包含一个贪心可行解
    initial_population = np.random.randint(0, np.max(gene_space_high), (sol_per_pop, num_genes))
    initial_population[0] = A_greed.flatten()

    # 创建遗传算法实例
    ga_instance = pygad.GA(
        num_generations=num_generations,  # 总共的进化代数
        num_parents_mating=num_parents_mating,  # 每一代中进行交配的父代数量
        fitness_func=fitness_function,  # 评价函数，用于评价每个候选解的适应度
        sol_per_pop=sol_per_pop,  # 种群中的个体数量
        num_genes=num_genes,  # 每个个体中的基因数量
        # init_range_low=init_range_low,  # 初始化基因时，基因值的最小范围
        # init_range_high=init_range_high,  # 初始化基因时，基因值的最大范围
        initial_population=initial_population, # 初始化种群
        parent_selection_type=parent_selection_type,  # 父代选择策略
        keep_parents=keep_parents,  # 下一代中保持的父代数量
        crossover_type=crossover_type,  # 交叉类型
        mutation_type=mutation_type,  # 变异类型
        mutation_percent_genes=mutation_percent_genes,  # 需要变异的基因的百分比
        gene_type=int,  # 基因的数据类型
        gene_space=gene_space,  # 可选的基因值范围
        stop_criteria=["saturate_1000"]  # 停止进化的条件
    )


    ga_instance.run()

    print("Number of generations passed is {generations_completed}".format(generations_completed= ga_instance.generations_completed))
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    solution.resize(X.shape)
    A = solution

    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print(f"Is constriants satisfied: {constraints_sati(A)}")
    # Prepare the data for the JSON output
    # Prepare the data for the JSON output
    data = []
    for m_index, m in enumerate(order_list):
        for n_index, n in enumerate(m['ckdata']):
            for k_index, k in enumerate(goods_list):
                if k == m['spnm']:  # We only need to add entries for the goods in the order
                    quantity = int(A[m_index][n_index][k_index])
                    dispatch_time = float(X[m_index][n_index][k_index] * A[m_index][n_index][k_index])
                    
                    # Do not append to data if quantity and dispatch time are 0
                    if quantity != 0 or dispatch_time != 0.0:
                        data.append({
                            "ddnm": m['ddnm'],  # order code
                            "cknm": n['cknm'],  # warehouse code
                            "qynm": m['qynm'],  # enterprise code
                            "spnm": k,  # goods code
                            "sl": quantity,  # quantity, convert numpy int64 to native Python int
                            "lg": goods_dict[m['spnm']] ,  # dimension not given in the data on 0705
                            "dpsj": dispatch_time,  # dispatch time, convert numpy float64 to native Python float if necessary
                        })

    # Package everything into a dict, ready for conversion to JSON
    result = {
        "code": 200,
        "data": data,
    }

    return json.dumps(result,ensure_ascii=False, indent=4)


def greedy_solution(X, Y, Z, O, W):
    """
    This function takes in five matrices X, Y, Z, O, W which represent
    different aspects of a logistics problem. The function should output a
    distribution plan to maximize overall satisfaction and minimize maximum
    transportation time greedily.

    Input:
    X: A 3D numpy array of shape (m, n, k) representing the unit transportation time
    Y: A 2D numpy array of shape (m, k) representing the demand for each type of good for each order
    Z: A 2D numpy array of shape (n, k) representing the stock of each type of good in each warehouse
    O: A 1D numpy array of length m representing the priority of each order
    W: A 1D numpy array of length n representing the priority of each warehouse

    Output:
    A distribution plan that maximizes overall satisfaction and minimizes maximum transportation time greedily.
    """
    Y = Y.copy()
    Z = Z.copy()
    A_greed = np.zeros_like(X)
    for i in range(A_greed.shape[0]):
        for k in range(A_greed.shape[2]):
            for j in range(A_greed.shape[1]):
                sati_ijk = np.minimum(Y[i,k], Z[j, k])
                A_greed[i,j,k] = sati_ijk
                Y[i,k] -= sati_ijk
                Z[j,k] -= sati_ijk
                if Y[i,k] <= 0:
                    break
            if Y[i,k] <= 0:
                break
    # print(np.sum(A_greed), A_greed)
    return A_greed



