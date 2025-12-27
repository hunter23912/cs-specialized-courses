#include "test.cpp"
#include "banker.cpp"
// 编程实现避免死锁算法：银行家算法

int main()
{
    test();
    return 0;
}
/*
3 3 2

max：
7 5 3
3 2 2
9 0 2
2 2 2
4 3 3

allocation：
0 1 0
2 0 0
3 0 2
2 1 1
0 0 2

// 安全序列1 3 4 2 0

p1请求
1 0 2

p0请求
0 2 0
*/