@startuml

actor 客户

box "客户提供的接口"
  participant "/queryYscb"
  participant "/ckylcxByUTC"
end box

box "我们的团队开发的接口"
  participant "/getZytpcl"
end box

客户 -> "/getZytpcl" : 提交订单列表
"/getZytpcl" -> "/queryYscb" : 查询运输成本
"/getZytpcl" -> "/ckylcxByUTC" : 查询库存信息
"/queryYscb" -> "/getZytpcl" : 返回运输成本
"/ckylcxByUTC" -> "/getZytpcl" : 返回库存信息
"/getZytpcl" -> 客户 : 返回最优调配策略
@enduml
