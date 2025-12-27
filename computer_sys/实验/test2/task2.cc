#include <omp.h>
#include <stdio.h>
#include <thread>

using namespace std;
#define MATRIX_SIZE 512 // 定义矩阵大小
#define TIMES 1e7       // 定义循环次数

// 计算两个size*size大小的矩阵的乘积
void compute(float *A, float *B, float *C, int size) // 两个矩阵相乘传统方法
{
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            C[4 * i + j] = A[4 * i + 0] * B[4 * 0 + j] + A[4 * i + 1] * B[4 * 1 + j] + A[4 * i + 2] * B[4 * 2 + j] +
                           A[4 * i + 3] * B[4 * 3 + j];
}

// OpenMP版本的矩阵乘法
void openmp_compute(float *A, float *B, float *C, int size, int num)
{
    double s, t, duration; // 定义时间变量
    s = omp_get_wtime();
#pragma omp parallel for num_threads(num)
    for (int n = 0; n < TIMES; n++) compute(A, B, C, size);
    t = omp_get_wtime();
    duration = (t - s) * 1000; // 计算耗时
    printf("Parallel %d :%.3fms\n", num, duration);
}

// 输出CPU支持的线程数
void PrintInfo()
{
    int num_threads = std::thread::hardware_concurrency(); // 获取系统支持的最大线程数
    omp_set_num_threads(num_threads);                      // 设置OpenMP线程数为系统支持的最大线程数
#pragma omp parallel
    {
        printf("Thread %d of %d\n", omp_get_thread_num(), omp_get_num_threads()); // 输出当前线程ID和总线程数
#pragma omp barrier                                                               // 等待所有线程到达此点
    }
    printf("Total threads: %d\n", num_threads); // 输出总线程数
}

int main()
{
    PrintInfo(); // 输出CPU支持的线程数

    int size = MATRIX_SIZE; // 矩阵大小
    // 动态分配内存
    float *A = new float[size * size]; // 分配内存
    float *B = new float[size * size]; // 分配内存
    float *C = new float[size * size]; // 分配内存

    // 初始化矩阵A和B,512x512大小的矩阵
    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
        {
            A[i * size + j] = i + j + 2;
            B[i * size + j] = (i + j + 2 * 1.0) / 1000;
        }
    double s, t, duration; // 定义时间变量

    // 先计算串行计算时间
    s = omp_get_wtime();
    for (int n = 0; n < TIMES; n++) compute(A, B, C, size);
    t = omp_get_wtime();
    duration = (t - s) * 1000;                // 计算耗时
    printf("Serial     :%.3fms\n", duration); // 输出串行计算时间

    // 调用函数进行OpenMP并行计算
    openmp_compute(A, B, C, size, 2);
    openmp_compute(A, B, C, size, 4);
    openmp_compute(A, B, C, size, 8);
    openmp_compute(A, B, C, size, 16);

    // 释放内存
    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}