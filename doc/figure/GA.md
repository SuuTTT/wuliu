@startuml
start
:初始化种群;
:计算适应度;
repeat
    :选择;
    :交叉;
    :突变;
    :计算适应度;
repeat while (未满足停止准则?)
stop
@enduml


@startuml
start
:初始化粒子群;
:计算适应度;
repeat
    :更新速度和位置;
    :边界检查;
    :计算适应度;
repeat while (未满足停止准则?)
stop
@enduml


@startuml
start
:初始化解和温度;
:计算适应度;
repeat
    :产生邻居解;
    :接受准则;
    :冷却计划;
    :计算适应度;
repeat while (未满足停止准则?)
stop
@enduml
