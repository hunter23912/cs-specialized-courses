#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define N 1024 // 矩阵大小（N x N）

// 初始化矩阵
void initialize_matrix(double *matrix, int size, double value)
{
    for (int i = 0; i < size * size; i++)
    {
        matrix[i] = value;
    }
}

// 打印矩阵的部分内容（仅前 5 行 5 列）
void print_matrix(double *matrix, int size)
{
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            printf("%f ", matrix[i * size + j]);
        }
        printf("\n");
    }
}

int main(int argc, char **argv)
{
    int rank, size;
    double *A, *B, *C_local;
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // 获取当前进程的主机名
    MPI_Get_processor_name(processor_name, &name_len);

    // 打印当前进程信息
    printf("Rank %d is running on host: %s\n", rank, processor_name);

    // 检查进程数是否合理
    if (N % size != 0)
    {
        if (rank == 0)
        {
            printf("Error: Number of processes must divide matrix size N.\n");
        }
        MPI_Finalize();
        return 1;
    }

    int block_size = N / size;

    // 分配本地矩阵空间
    A = (double *)malloc(N * block_size * sizeof(double));      // 每个进程处理 A 的一部分
    B = (double *)malloc(N * N * sizeof(double));               // 每个进程需要完整的 B
    C_local = (double *)calloc(block_size * N, sizeof(double)); // 本地结果矩阵

    // 初始化矩阵
    if (rank == 0)
    {
        double *A_full = (double *)malloc(N * N * sizeof(double));

        // 初始化 A 和 B
        initialize_matrix(A_full, N, 1.0); // A 的所有元素为 1.0
        initialize_matrix(B, N, 2.0);      // B 的所有元素为 2.0，直接初始化B而不是B_full

        // 将 A 分块发送到各个进程
        for (int i = 0; i < size; i++)
        {
            if (i == 0)
            {
                // 主进程直接复制自己的部分
                for (int j = 0; j < block_size * N; j++)
                {
                    A[j] = A_full[j];
                }
            }
            else
            {
                MPI_Send(&A_full[i * block_size * N], block_size * N, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
            }
        }

        free(A_full);

        printf("Rank 0 broadcasting matrix B to all processes...\n");
    }
    else
    {
        // 其他进程接收 A 的分块
        MPI_Recv(A, block_size * N, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    // 所有进程都使用相同的缓冲区B进行广播操作
    MPI_Bcast(B, N * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    printf("Rank %d received broadcast of matrix B.\n", rank);

    // 计算本地矩阵乘法
    printf("Rank %d starting local matrix multiplication...\n", rank);
    for (int i = 0; i < block_size; i++)
    {
        for (int j = 0; j < N; j++)
        {
            for (int k = 0; k < N; k++)
            {
                C_local[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }
    printf("Rank %d completed local matrix multiplication.\n", rank);

    // 收集结果到主进程
    double *C = NULL;
    if (rank == 0)
    {
        C = (double *)malloc(N * N * sizeof(double));
    }
    MPI_Gather(C_local, block_size * N, MPI_DOUBLE, C, block_size * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // 主进程输出结果
    if (rank == 0)
    {
        printf("Matrix multiplication completed. Result (first 5x5):\n");
        print_matrix(C, N);
        free(C);
    }

    free(A);
    free(B);
    free(C_local);

    MPI_Finalize();
    return 0;
}