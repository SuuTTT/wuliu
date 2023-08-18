@startuml

class Order {
  +OrderID : string
  +Company : string
  +Goods : List<Good>
}

class Warehouse {
  +WarehouseID : string
  +Goods : List<Good>
}

class Good {
  +GoodID : string
  +Quantity : int
  +Dimension : string
  +TransportTimePerUnit : Map<Warehouse, float>
}

class DistributionPlan {
  +OrderID : string
  +WarehouseID : string
  +Company : string
  +GoodID : string
  +Quantity : int
  +Dimension : string
  +DispatchTime : float
}

Order "1" -- "many" Good : contains >
Warehouse "1" -- "many" Good : contains >
Good "1" -- "many" Warehouse : transport time >
DistributionPlan -- Order : contains >
DistributionPlan -- Warehouse : contains >
DistributionPlan -- Good : contains >

@enduml
