#include <algorithm>
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

class PCB
{
public:
    string name;
    int arrival_time;
    int maxtime;
    int needtime;
    string state; // WAIT, RUNNING, FINISHED

    PCB(string _name, int at, int bt) : name(_name), arrival_time(at), maxtime(bt), needtime(bt), state("WAIT") {}
};

bool operator<(const PCB &a, const PCB &b)
{
    return a.arrival_time < b.arrival_time;
}

class RR
{
private:
    vector<PCB> queue;
    int time_slice = 1;

public:
    RR(int slice) : time_slice(slice) {}

    void add(const PCB &process)
    {
        queue.push_back(process);
        sort(queue.begin(), queue.end()); // 按照到达时间排序
    }

    void excute(PCB &pcb)
    {

        if (pcb.state == "WAIT")
        {
            int t = pcb.needtime - time_slice;
            if (t > 0)
            {
                pcb.needtime = t;
                pcb.state = "RUNNING";
            }
            else
            {
                pcb.needtime = 0;
                pcb.state = "FINISHED";
            }
        }
    }

    void renew(PCB &pcb)
    {
        if (pcb.state == "RUNNING")
            pcb.state = "WAIT";
    }

    void show()
    {
        printf("%-10s%-15s%-10s%-10s%-10s\n", "Name", "ArrivalTime", "MaxTime", "NeedTime", "State");
        for (auto p : queue)
        {
            printf("%-10s%-15d%-10d%-10d%-10s\n", p.name.c_str(), p.arrival_time, p.maxtime, p.needtime, p.state.c_str());
        }
    }

    void schedule()
    {
        if (queue.size())
        {
            PCB &current = queue.front();
            excute(current);
            show();
            renew(current);
            if (current.needtime)
                queue.push_back(current);
            queue.erase(queue.begin());
        }
    }
    bool check()
    {
        if (!queue.size())
            return true;
        return false;
    }
};

int main()
{
    int slice = 1;
    int k = 0;
    RR scheduler(slice); // 创建调度进程

    // 添加进程到调度器
    scheduler.add(PCB("d", 4, 6));
    scheduler.add(PCB("a", 0, 5));
    scheduler.add(PCB("b", 1, 3));
    scheduler.add(PCB("c", 3, 8));

    printf("initial state:\n");
    scheduler.show();

    // 循环等待用户输入
    while (!scheduler.check())
    {
        cin.get();
        k += slice;
        printf("CPUtime: %d\n", k);
        scheduler.schedule();
    }
    cout << "All processes have finished." << endl;
    return 0;
}
