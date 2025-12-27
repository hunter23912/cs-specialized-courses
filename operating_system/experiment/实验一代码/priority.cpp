#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

// 进程控制块（PCB）类
class PCB
{
public:
    string name;  // 进程名
    int priority; // 进程优先数
    int needtime; // 进程需要运行的时间
    int cputime;
    int maxtime;  // 占用CPU的时间
    string state; // 进程的状态

    // 构造函数
    PCB(string _name, int p, int nt)
        : name(_name), priority(p), needtime(nt), cputime(0), maxtime(nt), state("  READY") {}

    // 判断进程是否完成
    bool isFinished() const
    {
        return state == "  FINISHED";
    }

    // 每次调度执行时，更新进程信息
    string &execute()
    {
        if (state == "  READY")
        {
            cputime++;
            needtime--;
            if (needtime == 0)
                state = "  FINISHED";
            else
                state = "  RUNNING";
        }
        return state;
    }

    bool operator==(const PCB &other) const
    {
        return name == other.name;
    }
};

// 比较函数，用于优先队列
class ComparePCB
{
public:
    bool operator()(const PCB &p1, const PCB &p2)
    {
        // 优先级高的在前
        return p1.priority < p2.priority;
    }
};

// 进程调度类
class ProcessScheduler
{
private:
    priority_queue<PCB, vector<PCB>, ComparePCB> processes;
    vector<PCB> list;

public:
    // 添加进程到调度队列
    void addProcess(const PCB &pcb)
    {
        processes.push(pcb);
        list.push_back(pcb);
    }

    void update(auto &it, string &st)
    {
        it->cputime++;
        it->needtime--;
        it->priority -= 3;
        if (st == "  FINISHED")
            it->state = "->FINISHED<-";
        else if (st == "  RUNNING")
            it->state = "->RUNNING<-";
    }

    void renew(auto &it)
    {
        if (it->state == "->RUNNING<-")
            it->state = "  READY";
        if (it->state == "->FINISHED<-")
            it->state = "  FINISHED";
    }

    void print()
    {
        printf("%-10s %-10s %-10s %-10s %-10s %-10s\n", "ProcessID", "Maxtime", "Cputime", "Needtime", "Priority", "  State");
        for (auto &current : list)
            printf("%-10s %-10d %-10d %-10d %-10d %-10s\n", current.name.c_str(), current.maxtime, current.cputime, current.needtime, current.priority, current.state.c_str());
    }

    // 执行一次调度
    void scheduleOnce()
    {
        if (!processes.empty())
        {
            PCB current = processes.top();
            processes.pop();
            if (!current.isFinished())
            {
                string &t = current.execute();
                auto it = find(list.begin(), list.end(), current);
                if (it != list.end())
                {
                    update(it, t);
                    print();
                    renew(it);
                    if (!current.isFinished())
                        processes.push(*it);
                }
                else
                    cout << "error happened, scheduling failed" << endl;
                // 如果进程未完成，重新加入队列
            }
        }
    }
    bool check()
    {
        if (processes.empty())
            return true;
        return false;
    }
};

int main()
{
    // 创建调度器
    ProcessScheduler scheduler;

    // 创建进程并添加到调度器
    scheduler.addProcess(PCB("Process 1", 10, 10));
    scheduler.addProcess(PCB("Process 3", 40, 5));
    scheduler.addProcess(PCB("Process 2", 25, 8));
    scheduler.addProcess(PCB("Process 4", 90, 3));

    // 显示初始状态
    puts("Initial state:");
    scheduler.print();

    int k = 0;

    // 循环等待用户输入
    while (!scheduler.check())
    {
        cin.get();
        printf("CPUtime: %d\n", ++k); // 等待用户按下回车键
        scheduler.scheduleOnce();     // 执行一次调度
    }
    cout << "All processes have finished" << endl;
    return 0;
}
