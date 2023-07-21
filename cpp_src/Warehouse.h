#ifndef WAREHOUSE_H
#define WAREHOUSE_H

#include <string>
#include <vector>

class Warehouse {
private:
    std::string cknm; // 仓库内码
    std::vector<std::pair<std::string, int>> inventory; // {"商品内码", "数量"}
public:
    Warehouse(std::string cknm, std::vector<std::pair<std::string, int>> inventory) : cknm(cknm), inventory(inventory) {}
    std::string getCknm() { return cknm; }
    int getInventory(std::string spnm) {
        for(auto& item : inventory) {
            if(item.first == spnm) return item.second;
        }
        return 0;
    }
    void reduceInventory(std::string spnm, int sl) {
        for(auto& item : inventory) {
            if(item.first == spnm) {
                item.second -= sl;
                break;
            }
        }
    }
};

#endif
