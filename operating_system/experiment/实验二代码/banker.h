#pragma once
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;
class Banker
{
public:
    vector<int> Available;          // 可利用资源向量
    vector<vector<int>> Max;        // 最大需求矩阵
    vector<vector<int>> Allocation; // 已分配矩阵
    vector<vector<int>> Need;       // 需求矩阵

    // 默认构造函数
    Banker() {}

    Banker(vector<int> &available, vector<vector<int>> &_Max, vector<vector<int>> allocation);

    // 比较两个向量
    bool larger(vector<int> &a, vector<int> &b);

    // 相加两个向量
    void add(vector<int> &a, vector<int> &b);

    // 相减两个向量
    void sub(vector<int> &a, vector<int> &b);

    // 检查是否存在安全序列
    bool check(string &list);

    // 进程请求资源
    bool request(int pid, vector<int> &r);
};