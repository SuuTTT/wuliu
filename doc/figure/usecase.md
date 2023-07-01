@startuml
left to right direction
actor :用户: as customer
actor :系统管理员: as admin
rectangle "订单分配系统" {
    (配置系统) as config
    (输入订单数据) as enterOrder
    (输入仓库数据) as enterWarehouse
    (计算运输量和时间) as calc
    (查看结果) as view

    customer -- enterOrder
    customer -- enterWarehouse
    customer -- calc
    customer -- view
    admin -- config
}
@enduml
