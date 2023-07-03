@startuml
start

together {
    :初始化种群;
    :计算适应度;
}

together {
    repeat
        :选择;
        :交叉;
        :突变;
        :计算适应度;
    repeat while (未满足停止准则?)
}

stop
@enduml
