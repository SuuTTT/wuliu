#include "JsonParser.h"

std::vector<Order> JsonParser::parseOrders(json jsonData) {
    std::vector<Order> orders;
    for(auto& item : jsonData["spdd"]) {
        std::string ddnm = item["ddnm"];
        std::string qynm = item["qynm"];
        std::string spnm = item["spnm"];
        int sl = item["sl"];
        std::string lg = item["lg"];
        std::vector<std::pair<std::string, double>> ckdata;
        for(auto& ck : item["ckdata"]) {
            ckdata.push_back({ck["cknm"], ck["dwyssj"]});
        }
        orders.push_back(Order(ddnm, qynm, spnm, sl, lg, ckdata));
    }
    return orders;
}

std::vector<Warehouse> JsonParser::parseWarehouses(json jsonData) {
    std::vector<Warehouse> warehouses;
    for(auto& item : jsonData["ck"]) {
        for(auto& warehouse : item.items()) {
            std::string cknm = warehouse.key();
            std::vector<std::pair<std::string, int>> inventory;
            for(auto& good : warehouse.value()) {
                inventory.push_back({good["spnm"], good["sl"]});
            }
            warehouses.push_back(Warehouse(cknm, inventory));
        }
    }
    return warehouses;
}
