#include <omp.h> // 引入OpenMP头文件，提供并行处理的API
#include <stdio.h>
// openmp实验，测试openmp的并行计算能力

int main()
{
    int nthreads, tid;                      // 线程数和线程ID
    omp_set_num_threads(20);                // 设置线程数为8
#pragma omp parallel private(nthreads, tid) // 进入openmp的并行区域，并将nthreads和tid声明为私有变量
    {
        tid = omp_get_thread_num(); // 获取当前线程的ID
        printf("Hello World from OMP thread %d\n", tid);
        if (tid == 0)
        {
            nthreads = omp_get_num_threads();
            printf("Number of threads is %d\n", nthreads);
        }
    }
}
