#ifndef JSONPARSER_H
#define JSONPARSER_H

#include <string>
#include <vector>
#include "Order.h"
#include "Warehouse.h"
#include "Transport.h"
#include "json.hpp"

using json = nlohmann::json;

class JsonParser {
public:
    std::vector<Order> parseOrders(json jsonData);
    std::vector<Warehouse> parseWarehouses(json jsonData);
};

#endif
