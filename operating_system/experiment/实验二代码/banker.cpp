#include "banker.h"
#include <cstring>

// 含参构造函数
Banker::Banker(vector<int> &available, vector<vector<int>> &_Max, vector<vector<int>> allocation) : Available(available), Max(_Max), Allocation(allocation)
{
    int n = Max.size();
    Need.resize(n, vector<int>(Max[0].size(), 0));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < Max[i].size(); j++)
        {
            Need[i][j] = Max[i][j] - Allocation[i][j];
        }
    }
}

// 执行安全性检查
bool Banker::check(string &list)
{
    // cout << "成功进入check函数,开始安全性检查" << endl;
    int n = Max.size();
    int m = Available.size();
    vector<int> work = Available;
    bool finish[n] = {false};
    int num = 0;
    // cout << "预处理完成，即将进入循环" << endl;
    for (int i = 0; i < n; i++)
    {
        if (!finish[i])
        {
            if (larger(work, Need[i]))
            {
                add(work, Allocation[i]);
                finish[i] = true;
                list += "P" + to_string(i) + " ";
                num++;
                // cout << "当前finish:";
                // for (auto i : finish)
                //     cout << i << " ";
                // cout << endl;
                i = -1;
            }
        }
        if (num == n)
            return true;
    }
    return false;
}

// 进程请求资源实现
bool Banker::request(int pid, vector<int> &r)
{
    // 进程号过大，请求资源数量与可用资源数量不等
    if (pid < 0 || pid >= Max.size() || r.size() != Available.size())
    {
        cout << "Invalid request" << endl;
        return false;
    }

    // 请求资源数量超过最大需求或可用资源数量
    for (int i = 0; i < r.size(); i++)
    {
        if (r[i] > Need[pid][i] || r[i] > Available[i])
        {
            cout << "Request exceeds need or available resources." << endl;
            return false;
        }
    }

    // 请求合法，尝试分配资源
    cout << "Request is legal, trying allocation" << endl;
    sub(Available, r);
    add(Allocation[pid], r);
    sub(Need[pid], r);
    cout << "Trying finished, starting to check security" << endl;
    string list = "";
    // 如果不安全，恢复资源，报告信息
    if (!check(list))
    {
        add(Available, r);
        sub(Allocation[pid], r);
        add(Need[pid], r);
        cout << "Request Failed! it would lead to an unsafe state." << endl;
        return false;
    }
    cout << "Request Succeed!" << endl;
    cout << "After allocation, one safe sequence: " << list << endl;
    return true;
}

/// @brief 比较向量大小
/// @param a
/// @param b
/// @return a > b返回true
bool Banker::larger(vector<int> &a, vector<int> &b)
{
    for (int i = 0; i < a.size(); i++)
    {
        if (a[i] < b[i])
            return false;
    }
    return true;
}

// 向量相加实现
void Banker::add(vector<int> &a, vector<int> &b)
{
    for (int i = 0; i < a.size(); i++)
        a[i] += b[i];
}

// 向量相减
void Banker::sub(vector<int> &a, vector<int> &b)
{
    for (int i = 0; i < a.size(); i++)
        a[i] -= b[i];
}