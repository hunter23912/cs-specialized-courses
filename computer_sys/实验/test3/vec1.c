#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define N 1000000 // 向量大小

int main(int argc, char **argv)
{
    int rank, size;
    double *a, *b;
    double local_dot = 0.0, global_dot = 0.0;

    MPI_Init(&argc, &argv); // 初始化MPI环境
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // 获取当前进程编号
    MPI_Comm_size(MPI_COMM_WORLD, &size); // 获取进程总数

    // 计算每个进程负责的数据块大小
    int local_size = N / size; // 每个进程的基本数据块大小
    int remainder = N % size; // 剩余数据块大小

    // 调整最后一个进程的数据块大小
    if (rank == size - 1)
    {
        local_size += remainder;
    } 

    // 分配本地向量空间
    a = (double *)malloc(local_size * sizeof(double));
    b = (double *)malloc(local_size * sizeof(double));

    // 初始化本地向量数据
    for (int i = 0; i < local_size; i++)
    {
        a[i] = 1.0;
        b[i] = 1.0;
    }

    // 计算本地点积
    for (int i = 0; i < local_size; i++)
    {
        local_dot += a[i] * b[i];
    }

    // 全局归约求和，将所有进程的local_dot相加到rank==0的global_dot中
    MPI_Reduce(&local_dot, &global_dot, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    // 主进程输出结果
    if (rank == 0)
    {
        printf("Dot product result: %f\n", global_dot);
    }

    free(a);
    free(b);
    MPI_Finalize();
    return 0;
}