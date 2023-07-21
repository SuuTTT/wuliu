#ifndef ORDER_H
#define ORDER_H

#include <string>
#include <vector>

class Order {
private:
    std::string ddnm; // 订单内码
    std::string qynm; // 企业内码
    std::string spnm; // 商品内码
    int sl; // 数量
    std::string lg; // 量纲
    std::vector<std::pair<std::string, double>> ckdata; // {"仓库内码", "单位运输时间"}
public:
    Order(std::string ddnm, std::string qynm, std::string spnm, int sl, std::string lg, std::vector<std::pair<std::string, double>> ckdata)
        : ddnm(ddnm), qynm(qynm), spnm(spnm), sl(sl), lg(lg), ckdata(ckdata) {}
    std::string getDdnm() { return ddnm; }
    std::string getQynm() { return qynm; }
    std::string getSpnm() { return spnm; }
    int getSl() { return sl; }
    std::string getLg() { return lg; }
    double getTransportTime(std::string cknm) {
        for(auto& ck : ckdata) {
            if(ck.first == cknm) return ck.second;
        }
        return 0;
    }
};

#endif
