#pragma once
#include "banker.h"
#include <stdexcept>
using namespace std;

// 一些函数声明
void test();
Banker Init();
void Request(Banker &banker);
void PrintMatrix(Banker &b);

// 打印矩阵信息相关函数
string sMax(vector<int> &v);
string sAllocation(vector<int> &v);
string sNeed(vector<int> &v);