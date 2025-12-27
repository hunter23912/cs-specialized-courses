#include "test.h"

void test()
{
    Banker banker;
    while (true)
    {
        printf("-----银行家算法-----\n");
        printf("1. Init\n");
        printf("2. Request\n");
        printf("3. IsSafe\n");
        printf("4. PrintMatrix\n");
        printf("5. Exit\n");
        printf("--------------------\n");
        printf("Please select: ");
        char c;
        cin >> c;
        switch (c)
        {
        case '1':
        {
            banker = Init();
            break;
        }
        case '2':
        {
            Request(banker);
            break;
        }
        case '3':
        {
            string list = "";
            if (banker.check(list))
            {
                cout << "Safe now!" << endl;
                cout << "One safe sequence:" << list << endl;
            }
            else
                cout << "Unsafe now!" << endl;
            break;
        }
        case '4':
        {
            PrintMatrix(banker);
            break;
        }
        case '5':
            exit(0);
        }
    }
}

// 如果键入1，则初始化银行家算法
Banker Init()
{
    // 输入available
    cout << "Please input the available(A B C):";
    int a, b, c;
    cin >> a >> b >> c;
    // a = 3, b = 3, c = 2;
    vector<int> available = {a, b, c};

    // 输入max
    vector<vector<int>> max_demands = {};
    int n;
    cout << "Please enter the number of processes:";
    cin >> n;
    // n = 5;
    cout << "Initialize Max matrix:" << endl;
    for (int i = 0; i < n; i++)
    {
        cin >> a >> b >> c;
        max_demands.push_back({a, b, c});
    }
    // a = 7, b = 5, c = 3;
    // max_demands.push_back({a, b, c});
    // a = 3, b = 2, c = 2;
    // max_demands.push_back({a, b, c});
    // a = 9, b = 0, c = 2;
    // max_demands.push_back({a, b, c});
    // a = 2, b = 2, c = 2;
    // max_demands.push_back({a, b, c});
    // a = 4, b = 3, c = 3;
    // max_demands.push_back({a, b, c});

    // 输入allocation
    cout << "Initialize Allocation matrix:" << endl;
    vector<vector<int>> Allocation = {};
    for (int i = 0; i < n; i++)
    {
        cin >> a >> b >> c;
        Allocation.push_back({a, b, c});
    }
    // a = 0, b = 1, c = 0;
    // Allocation.push_back({a, b, c});
    // a = 2, b = 0, c = 0;
    // Allocation.push_back({a, b, c});
    // a = 3, b = 0, c = 2;
    // Allocation.push_back({a, b, c});
    // a = 2, b = 1, c = 1;
    // Allocation.push_back({a, b, c});
    // a = 0, b = 0, c = 2;
    // Allocation.push_back({a, b, c});
    cout << "已初始化完成" << endl;
    Banker banker(available, max_demands, Allocation);
    return banker;
}

// 如果输入2，则请求资源
void Request(Banker &banker)
{
    int pid;
    cout << "Please input the process ID: P";
    cin >> pid;
    cout << "Please input the request(A B C):";
    int a, b, c;
    cin >> a >> b >> c;
    vector<int> r = {a, b, c};
    banker.request(pid, r);
}

string sMax(vector<int> &v)
{
    string s = "";
    for (int i = 0; i < v.size(); i++)
        s += to_string(v[i]) + " ";
    return s;
}

string sAllocation(vector<int> &v)
{
    string s = "  ";
    for (int i = 0; i < v.size(); i++)
        s += to_string(v[i]) + " ";
    return s;
}

string sNeed(vector<int> &v)
{
    string s = "";
    for (int i = 0; i < v.size(); i++)
        s += to_string(v[i]) + " ";
    return s;
}

// 如果输入4，则打印所有进程资源信息
void PrintMatrix(Banker &b)
{
    int n = b.Max.size();
    printf("Available(A B C):");
    for (int i = 0; i < 3; i++)
    {
        cout << b.Available[i] << " ";
    }
    cout << endl;
    printf("%-9s%-8s%-12s%-10s\n", "Process", " Max", "Allocation", "Need");
    for (int i = 0; i < n; i++)
    {
        string process = "  P" + to_string(i);
        vector<int> v1 = b.Max[i];
        vector<int> v2 = b.Allocation[i];
        vector<int> v3 = b.Need[i];
        printf("%-9s%-8s%-12s%-10s\n", process.c_str(), sMax(v1).c_str(), sAllocation(v2).c_str(), sNeed(v3).c_str());
    }
}