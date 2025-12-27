#include <iostream>
#include <vector>
#include <cstring>
#include <queue>
#include <algorithm>
using namespace std;
// 请求页式存储管理

const int N = 110; // 最大地址数

const int MAX_ADDR = 1048575; // 最大虚拟地址为2^20-1
const int PAGE_SIZE = 1024;   // 页大小
int vir_addr[N];              // 虚拟地址数组
int page[N];                  // 页号数组
char res[N][N];               // 显示数组
void vir_addr_to_page()
{
    srand(static_cast<int>(time(0)));
    int n = 10;
    for (int i = 1; i <= n; i++)
    {
        // 生成随机地址
        int t1 = rand() % MAX_ADDR;
        vir_addr[i] = t1;
        // 获取页号
        page[i] = t1 / PAGE_SIZE;
    }
    cout << "虚拟地址流:" << endl;
    for (int i = 1; i <= n; i++)
    {
        printf("vir_addr[%d] = %-10d", i, vir_addr[i]);
        cout << (i % 4 == 0 ? "\n" : "    ");
    }
    cout << endl;
    cout << "页号流:" << endl;
    for (int i = 1; i <= n; i++)
    {
        printf("page[%d] = %-5d", i, page[i]);
        cout << (i % 4 == 0 ? "\n" : " ");
    }
    cout << endl;
}

// show
double show(vector<int> &list, int memory_num, int page_fault)
{
    int n = list.size();
    cout << "结果序列:" << endl;
    for (int i = 0; i <= memory_num; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cout << res[i][j] << " ";
        }
        cout << endl;
    }
    cout << "缺页数为:" << page_fault << endl;
    double rate = (double)page_fault / n;
    cout << "缺页率为:" << rate << endl;
    return rate;
}

// FIFO算法
int FIFO(vector<int> &list, int memory_num)
{
    int n = list.size();
    int page_fault = 0; // 缺页数
    deque<int> q;
    vector<int> memory;
    int k = 0;
    memset(res, '_', sizeof(res));
    for (auto &x : list)
    {
        bool flag = false;
        bool isfull = false;
        char change;
        for (auto &y : memory)
        {
            if (y == x)
            {
                flag = true;
                res[memory_num][k] = 'T';
                k++;
                break;
            }
        }
        // 如果x不在内存中
        if (!flag)
        {
            res[memory_num][k] = 'F';
            page_fault++;
            if (memory.size() < memory_num)
            {
                memory.push_back(x);
                q.push_back(x);
            }
            else
            {
                isfull = true;
                change = q.front();
                q.pop_front();
                q.push_back(x);
                for (auto &y : memory)
                    if (y == change)
                        y = x;
            }
            // 更新res数组,如果flag为true,则不更新
            for (int i = 0; i < memory.size(); i++)
                res[i][k] = memory[i] + '0';
            k++;
        }
    }
    return page_fault;
}

// OPT算法
int OPT(vector<int> &list, int memory_num)
{
    int n = list.size();
    int page_fault = 0; // 缺页数
    vector<int> memory;
    int k = 0;
    memset(res, '_', sizeof(res));
    // 遍历整个请求页面好序列
    for (int i = 0; i < n; i++)
    {
        int &x = list[i];
        bool flag = false;
        for (auto &y : memory)
        {
            if (y == x)
            {
                flag = true;
                res[memory_num][k] = 'T';
                k++;
                break;
            }
        }
        // 如果x不在内存中
        if (!flag)
        {
            res[memory_num][k] = 'F';
            page_fault++;
            if (memory.size() < memory_num)
                memory.push_back(x);
            else
            {
                // 找到序列中在memory里最远的页号
                int s[n], top = 0;
                bool st[memory_num];
                memset(st, false, sizeof(st));
                for (int j = i + 1; j < n; j++)
                {
                    int x2 = list[j];
                    // 对后续序列中的每项，遍历内存块
                    for (int u = 0; u < memory.size(); u++)
                    {
                        int &y = memory[u];
                        if (y == x2)
                        {
                            if (!st[u])
                            {
                                st[u] = true;
                                s[top++] = y;
                            }
                        }
                    }
                }
                top--;

                // 找到后，更新内存块中指定块的内容
                bool done = false;
                for (int u = 0; u < memory_num; u++)
                    if (!st[u])
                    {
                        memory[u] = x;
                        done = true;
                        break;
                    }
                if (done == false)
                {
                    for (auto &y : memory)
                        if (y == s[top])
                            y = x;
                }
            }
            // 更新res数组
            for (int i = 0; i < memory.size(); i++)
                res[i][k] = memory[i] + '0';
            k++;
        }
    }
    return page_fault;
}

int LRU(vector<int> &list, int memory_num)
{
    int n = list.size();
    int page_fault = 0; // 缺页数
    vector<int> memory;
    int k = 0;
    memset(res, '_', sizeof(res));
    // 遍历整个请求页面好序列
    for (int i = 0; i < n; i++)
    {
        int &x = list[i];
        bool flag = false;
        for (auto &y : memory)
        {
            if (y == x)
            {
                flag = true;
                res[memory_num][k] = 'T';
                k++;
                break;
            }
        }
        // 如果x不在内存中
        if (!flag)
        {
            res[memory_num][k] = 'F';
            page_fault++;
            if (memory.size() < memory_num)
                memory.push_back(x);
            else // memory已满，向左找，一定能找到
            {
                // 找到序列中在memory里最远的页号
                int top;
                bool st[memory_num];
                memset(st, false, sizeof(st));
                for (int j = i - 1; j >= 0; j--)
                {
                    int x2 = list[j];
                    // 对后续序列中的每项，遍历内存块
                    int cnt = 0;
                    for (int u = 0; u < memory.size(); u++)
                    {
                        int &y = memory[u];
                        if (y == x2)
                        {
                            if (!st[u])
                            {
                                st[u] = true;
                                top = y;
                                cnt++;
                                if (cnt == memory_num)
                                    break;
                            }
                        }
                    }
                }
                // 找到后，更新内存块中指定块的内容
                for (auto &y : memory)
                    if (y == top)
                    {
                        y = x;
                        break;
                    }
            }
            // 更新res数组
            for (int i = 0; i < memory.size(); i++)
                res[i][k] = memory[i] + '0';
            k++;
        }
    }
    return page_fault;
}

void compare(vector<int> &list)
{
    for (int memory_num = 3; memory_num <= 5; memory_num++)
    {
        cout << "==================================================" << endl;
        cout << "页面大小: 1024B  内存块数: " << memory_num << endl;
        int n = list.size();
        int num_FIFO = FIFO(list, memory_num);
        double rate_FIFO = num_FIFO / (double)n;
        double hit_FIFO = 1 - rate_FIFO;
        int num_OPT = OPT(list, memory_num);
        double rate_OPT = num_OPT / (double)n;
        double hit_OPT = 1 - rate_OPT;
        int num_LRU = LRU(list, memory_num);
        double rate_LRU = num_LRU / (double)n;
        double hit_LRU = 1 - rate_LRU;
        printf("OPT    缺页数: %-3d    缺页率: %-4.3lf    命中率: %-4.3lf\n", num_FIFO, rate_FIFO, hit_FIFO);
        printf("FIFO   缺页数: %-3d    缺页率: %-4.3lf    命中率: %-4.3lf\n", num_OPT, rate_OPT, hit_OPT);
        printf("LRU    缺页数: %-3d    缺页率: %-4.3lf    命中率: %-4.3lf\n", num_LRU, rate_LRU, hit_LRU);
    }
}
