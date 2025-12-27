#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std;
typedef pair<string, int> PII;
#define x first
#define y second

// 分区结构体
struct Partition
{
    int size;         // 剩余分区大小
    int startAddress; // 起始地址
    bool free = true; // 是否空闲
    vector<PII> list;
};

// 首次适应算法
int firstFit(vector<Partition> &memory, string &name, int processSize)
{
    for (auto &part : memory)
        if (part.size >= processSize)
        {
            if (part.free)
                part.free = false;
            part.list.push_back({name, processSize});
            int tmp = part.size - processSize;
            if (tmp < 0)
                break;
            part.size = tmp;
            return part.startAddress;
        }
    return -1; // 没有足够的空间
}

// 循环首次适应算法
int nextFit(vector<Partition> &memory, string &name, int processSize, int &nextIndex)
{
    for (int i = 0; i < memory.size(); i++)
    {
        int index = (i + nextIndex) % memory.size();
        auto &val = memory[index];
        if (val.size >= processSize)
        {
            if (val.free)
                val.free = false;
            val.list.push_back({name, processSize});
            val.free = false;
            int tmp = val.size - processSize;
            if (tmp < 0)
                break;
            val.size = tmp;
            nextIndex = index + 1;
            return val.startAddress;
        }
    }
    return -1;
}

// 最佳适应算法
int bestFit(vector<Partition> &memory, string &name, int processSize)
{
    int bestIndex = -1;
    int minSize = INT_MAX;
    for (int i = 0; i < memory.size(); i++)
    {
        if (memory[i].size >= processSize && memory[i].size < minSize)
        {
            bestIndex = i;
            minSize = memory[i].size;
        }
    }
    if (bestIndex != -1)
    {
        auto &val = memory[bestIndex];
        val.list.push_back({name, processSize});
        if (val.free)
            val.free = false;
        int tmp = val.size - processSize;
        if (tmp < 0)
            return -1;
        val.size = tmp;
        return val.startAddress;
    }
    return -1;
}

// 最坏适应算法
int worstFit(vector<Partition> &memory, string &name, int processSize)
{
    int worstIndex = -1;
    int maxSize = 0;
    for (int i = 0; i < memory.size(); i++)
    {
        if (memory[i].size >= processSize && memory[i].size > maxSize)
        {
            worstIndex = i;
            maxSize = memory[i].size;
        }
    }
    if (worstIndex != -1)
    {
        auto &val = memory[worstIndex];
        val.list.push_back({name, processSize});
        if (val.free)
            val.free = false;
        int tmp = val.size - processSize;
        if (tmp < 0)
            return -1;
        val.size = tmp;
        return val.startAddress;
    }
    return -1;
}

//  回收内存分配算法
bool recycle(vector<Partition> &memory, string &name)
{
    for (auto &part : memory)
    {
        if (part.free)
            continue;
        for (auto &cur : part.list)
        {
            if (cur.x == name)
            {
                part.size += cur.y;
                part.list.erase(find(part.list.begin(), part.list.end(), cur));
                if (part.list.empty())
                    part.free = true;
                return true;
            }
        }
    }
    return false;
}