#include "solution.cpp"
#include <cstdio>
#include <sstream>
// 请求页式存储管理

int main()
{
    while (true)
    {
        cout << "选择测试任务:" << endl;
        cout << "1. 虚拟地址求页号" << endl;
        cout << "2. 页面置换算法" << endl;
        cout << "3. 比较不同置换算法缺页率" << endl;
        cout << "4. 退出" << endl;
        char c;
        cin >> c;
        switch (c)
        {
        case '1':
        {
            vir_addr_to_page();
            break;
        }
        case '2':
        {
            int memory_num = 3;
            cout << "请输入内存块数:";
            cin >> memory_num;
            cout << "请选择页面置换算法:" << endl;
            cout << "1. FIFO" << endl;
            cout << "2. OPT" << endl;
            cout << "3. LRU" << endl;
            cout << "4. 退出" << endl;
            char c2;
            cin >> c2;

            cout << "请输入页面号序列:" << endl;
            string s;
            getline(cin, s); // 读取换行符
            getline(cin, s);
            stringstream ssin(s);
            int number;
            vector<int> list;
            // list = {4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1, 5};
            while (ssin >> number)
                list.push_back(number);

            switch (c2)
            {
            case '1':
            {
                int page_fault = FIFO(list, memory_num);
                show(list, memory_num, page_fault);
                break;
            }
            case '2':
            {
                int page_fault = OPT(list, memory_num);
                show(list, memory_num, page_fault);
                break;
            }
            case '3':
            {
                int page_fault = LRU(list, memory_num);
                show(list, memory_num, page_fault);
                break;
            }
            case '4':
                break;
            }
            break;
        }
        case '3': // 比较不同置换算法缺页率
        {
            cout << "请输入页面号序列:" << endl;
            string s;
            getline(cin, s); // 读取换行符
            getline(cin, s);
            stringstream ssin(s);
            int number;
            vector<int> list;
            // list = {4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1, 5};
            while (ssin >> number)
                list.push_back(number);
            compare(list);
            break;
        }
        case '4':
            exit(0);
        }
    }
    return 0;
}