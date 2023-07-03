import numpy as np
import pygad

def logistics_distribution(A1, A2, A3, W1, W2):
    """
    This function takes in five matrices A1, A2, A3, W1, W2 which represent 
    different aspects of a logistics problem. The function should output a 
    distribution plan to maximize overall satisfaction and minimize maximum 
    transportation time.
    
    Input:
    A1: A 3D numpy array of shape (m, n, k) representing the unit transportation time
    A2: A 2D numpy array of shape (m, k) representing the demand for each type of good for each order
    A3: A 2D numpy array of shape (n, k) representing the stock of each type of good in each warehouse
    W1: A 1D numpy array of length m representing the priority of each order
    W2: A 1D numpy array of length n representing the priority of each warehouse
    
    Output:
    A distribution plan that maximizes overall satisfaction and minimizes maximum transportation time.
    """

    # 设置满足度和运输时间的权重
    alpha = 0.99
    beta = 0.01
    
    # 初始化解向量 X
    X = np.zeros_like(A1, dtype=int)
    
    # 处理订单需求数据
    A2_copy = A2.copy()
    A2_copy[np.where(A2==0)] = np.inf
    
    # 定义约束的判断函数
    def constraints_sati(X):
        X.resize(A1.shape)
        if (np.sum(X, axis=0) < 0).any():
            print(f"np.sum(X, axis=0){np.sum(X, axis=0)}")
            return False
        elif ((np.sum(X, axis=0) - A3) > 0).any():
            print(f"np.sum(X, axis=0) - A3{np.sum(X, axis=0) - A3}")
            return False
        elif (np.sum(X, axis=1) < 0).any():
            print(f"np.sum(X, axis=1){np.sum(X, axis=1)}")
            return False
        elif ((np.sum(X, axis=1) - A2) > 0).any():
            print(f"(np.sum(X, axis=1) - A2){(np.sum(X, axis=1))}")
            return False
        else:
            return True
            # Y = X * A1
            # fitness_sati = alpha * np.sum(W1 * np.sum(np.sum(X * W2[np.newaxis,:,np.newaxis], axis=1) / A2_copy, axis=-1), axis=0)
            # fitness_time = beta * np.max(np.sum(Y, axis=(1,2)))
            # fitness = fitness_sati - fitness_time
            # return fitness
    # 定义带有惩罚项的满足度计算函数
    def fitness_func_penalty(ga_instance, X, X_idx):  # X is solution
        # setting constraints
        X.resize(A1.shape)
        penalty = 0

        # adjust the penalties based on your requirements
        if (np.sum(X, axis=0) < 0).any():
            penalty += np.sum(np.abs(np.sum(X, axis=0)[np.sum(X, axis=0) < 0]))
        if ((np.sum(X, axis=0) - A3) > 0).any():
            penalty += np.sum(np.abs(np.sum(X, axis=0) - A3)[(np.sum(X, axis=0) - A3) > 0])
        if (np.sum(X, axis=1) < 0).any():
            penalty += np.sum(np.abs(np.sum(X, axis=1)[np.sum(X, axis=1) < 0]))
        if ((np.sum(X, axis=1) - A2) > 0).any():
            penalty += np.sum(np.abs(np.sum(X, axis=1) - A2)[(np.sum(X, axis=1) - A2) > 0])

        Y = X * A1
        fitness_sati = alpha * np.sum(W1 * np.sum(np.sum(X * W2[np.newaxis, :, np.newaxis], axis=1) / A2_copy, axis=-1),
                                      axis=0)
        fitness_time = beta * np.max(np.sum(Y, axis=(1, 2)))
        fitness = fitness_sati - fitness_time - penalty

        return fitness
    # 设置使用带有惩罚项的满足度计算函数
    fitness_function = fitness_func_penalty

    # 设置遗传算法的参数
    num_generations = 5000         # 迭代次数
    num_parents_mating = 4         # 交配的父母数量
    sol_per_pop = 8                # 种群中的解的数量
    num_genes = X.shape[0]*X.shape[1]*X.shape[2]  # 每个解中的基因数量
    init_range_low = -2            # 初始化解的下限
    init_range_high = 5            # 初始化解的上限
    parent_selection_type = "sss"  # 选择父母的类型
    keep_parents = 1               # 保留父母的数量
    crossover_type = "single_point" # 交叉类型
    mutation_type = "random"       # 变异类型
    mutation_percent_genes = 30    # 变异基因的百分比
    # 计算基因空间的上限
    gene_space_high = np.minimum(A2[:,np.newaxis,:], A3[np.newaxis,:,:]).flatten().tolist()
    gene_space = [np.arange(0, int(high+1)) for high in gene_space_high]

    # 创建遗传算法实例
    ga_instance = pygad.GA(
        num_generations=num_generations,  # 总共的进化代数
        num_parents_mating=num_parents_mating,  # 每一代中进行交配的父代数量
        fitness_func=fitness_function,  # 评价函数，用于评价每个候选解的适应度
        sol_per_pop=sol_per_pop,  # 种群中的个体数量
        num_genes=num_genes,  # 每个个体中的基因数量
        init_range_low=init_range_low,  # 初始化基因时，基因值的最小范围
        init_range_high=init_range_high,  # 初始化基因时，基因值的最大范围
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

    solution.resize(A1.shape)
    X = solution

    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print(f"Is constriants satisfied: {constraints_sati(X)}")
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            print(f"For order {i}, warehouse {j}, the transportation quantity are {X[i,j]} for goods [1,2]")