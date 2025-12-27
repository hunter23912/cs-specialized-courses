#include "solution.cpp"
#include <cstdio>

void show(vector<Partition> &memory)
{
    printf("%-10s%-10s%-12s%-18s\n", "分区号", "大小", "起始地址", "状态");
    for (int i = 0; i < memory.size(); i++)
    {
        string s = "空闲";
        if (!memory[i].free)
        {
            s = "占用(";
            for (auto &cur : memory[i].list)
                s += cur.x + ",";
            s.pop_back();
            s += ")";
        }
        printf("%-10d%-10d%-12d%-18s\n", i, memory[i].size, memory[i].startAddress, s.c_str());
    }
}

void choosefunc(vector<Partition> &memory, string &name, int &currentSize, int &nextIndex, char &choice, int &flag)
{
    switch (choice)
    {
    case '1':
    {
        flag = firstFit(memory, name, currentSize);
        break;
    }
    case '2':
    {
        flag = nextFit(memory, name, currentSize, nextIndex);
        break;
    }
    case '3':
    {
        flag = bestFit(memory, name, currentSize);
        break;
    }
    case '4':
    {
        flag = worstFit(memory, name, currentSize);
        break;
    }
    }
}

int main()
{
    vector<Partition> memory = {
        {40, 0},
        {100, 40},
        {350, 140},
        {150, 490}};
    int nextIndex = 0;
    while (true)
    {
        cout << "----------分配前的分区列表----------" << endl;
        show(memory);
        printf("1.首次适应算法\n");
        printf("2.循环首次适应算法\n");
        printf("3.最佳适应算法\n");
        printf("4.最坏适应算法\n");
        printf("5.退出\n");
        printf("请选择分配算法:");
        char choice;
        cin >> choice;
        if (choice == '5')
            exit(0);
        while (true)
        {
            cout << "-------" << endl;
            cout << "|1.分配|" << endl;
            cout << "|2.回收|" << endl;
            cout << "|3.返回|" << endl;
            cout << "-------" << endl;
            char c;
            cin >> c;
            if (c == '1')
            {
                string name = "NULL";
                int currentSize = 0;
                cout << "请输入作业名:";
                cin >> name;
                cout << "请输入作业大小:";
                cin >> currentSize;
                int flag = -1;
                choosefunc(memory, name, currentSize, nextIndex, choice, flag);
                if (flag == -1)
                    cout << "没有足够的空间" << endl;
                else
                {
                    cout << "分配成功,分配的起始地址为:" << flag << endl;
                    cout << "----------成功分配后的分区列表----------" << endl;
                    show(memory);
                }
            }
            else if (c == '2')
            {
                bool flag = false;
                cout << "请输入要回收的作业名:";
                string name;
                cin >> name;
                flag = recycle(memory, name);
                if (flag == false)
                    cout << "回收失败,无可回收空间" << endl;
                else if (flag == true)
                {
                    cout << "回收成功!" << endl;
                    cout << "---------回收后的分区列表---------" << endl;
                    show(memory);
                }
            }
            else if (c == '3')
                break;
        }
    }
    return 0;
}