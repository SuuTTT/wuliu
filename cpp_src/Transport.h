#ifndef TRANSPORT_H
#define TRANSPORT_H

#include <string>

class Transport {
private:
    std::string ddnm; // 订单内码
    std::string cknm; // 仓库内码
    std::string qynm; // 企业内码
    std::string spnm; // 商品内码
    int sl; // 数量
    std::string lg; // 量纲
    double dpsj; // 调配时间
public:
    Transport(std::string ddnm, std::string cknm, std::string qynm, std::string spnm, int sl, std::string lg, double dpsj)
        : ddnm(ddnm), cknm(cknm), qynm(qynm), spnm(spnm), sl(sl), lg(lg), dpsj(dpsj) {}
    std::string getDdnm() { return ddnm; }
    std::string getCknm() { return cknm; }
    std::string getQynm() { return qynm; }
    std::string getSpnm() { return spnm; }
    int getSl() { return sl; }
    std::string getLg() { return lg; }
    double getDpsj() { return dpsj; }
};

#endif
