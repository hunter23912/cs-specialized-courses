#include <iostream>
#include <omp.h> // OpenMP头文件
#include <thread>
#include <time.h>

// 一个简单的函数，用于模拟计算密集型任务
double calculate_pi(int num_steps)
{
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;

#pragma omp parallel for reduction(+ : sum)
    for (int i = 0; i < num_steps; i++)
    {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }
    std::cout << "并行任务数量 " << num_steps << std::endl;
    return step * sum;
}

// 串行计算π的近似值
double cal_pi_serial(int num_steps)
{
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;
    for (int i = 0; i < num_steps; i++)
    {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }
    std::cout << "迭代了 " << num_steps << " 次" << std::endl;
    return step * sum;
}

int main()
{
    // 获取系统信息
    int num_threads = std::thread::hardware_concurrency(); // 获取系统支持的最大线程数

    std::cout << "系统处理器数量: " << num_threads << std::endl;

    // 设置OpenMP线程数为处理器数量
    omp_set_num_threads(num_threads); // 设置OpenMP线程数为处理器数量

    const int num_steps = 100000000; // 1亿次迭代

    // 串行计算π的近似值
    clock_t s_time_serial = clock();
    double pi_serial = cal_pi_serial(num_steps);
    clock_t e_time_serial = clock();
    double elapsed_time_serial = (double)(e_time_serial - s_time_serial) / CLOCKS_PER_SEC * 1000; // 转换为毫秒
    std::cout << "串行计算π的近似值: " << pi_serial << std::endl;
    std::cout << "串行计算耗时: " << elapsed_time_serial << " 毫秒" << std::endl;

    // 并行计算π的近似值
    clock_t s_time_parallel = clock();
    double pi = calculate_pi(num_steps);
    clock_t e_time_parallel = clock();
    double elapsed_time_parallel = (double)(e_time_parallel - s_time_parallel) / CLOCKS_PER_SEC * 1000; // 转换为毫秒
    std::cout << "并行计算π的近似值: " << pi << std::endl;
    std::cout << "并行计算耗时: " << elapsed_time_parallel << " 毫秒" << std::endl;
    std::cout << "加速比: " << elapsed_time_serial / elapsed_time_parallel << std::endl;
    return 0;
}