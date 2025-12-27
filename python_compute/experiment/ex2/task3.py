import random

def birthday_ex(M,N):
    '''
    进行生日相同概率实验
    :param M: 班级数量
    :param N: 每个班级的学生数量
    :return: 生日相同的概率
    '''
    Q = 0 # 存在相同生日的班级数
    for _ in range(M):
        # 生成一个班级的N个生日
        birthdays = [random.randint(1, 365) for _ in range(N)]
        
        # 判断是否有相同生日
        if len(birthdays) != len(set(birthdays)):
            Q += 1
    # 计算生日相同的概率
    P = Q / M
    return P

def main():
    print("===生日相同概率分析===")
    
    # 获取用户输入
    M = int(input("请输入班级数量M(M>=1000)："))
    while M < 1000:
        print("M必须大于等于1000")
        M = int(input("请重新输入班级数量M(M>=1000)："))
        
    N = int(input("请输入每个班级的学生数量N(N>=2)："))
    
    probability = birthday_ex(M, N)
    
    # 输出结果
    print(f'\n实验结果:')
    print(f'班级数量M：{M}')
    print(f'每个班级的学生数量N：{N}')
    print(f'存在相同生日的班级数：{int(probability * M)}')
    print(f'生日相同的概率：{probability:.4f} ({probability * 100:.2f}%)')
    
    # 理论概率统计
    if N <= 365:
        theoretical_p = 1.0
        for i in range(1, N):
            theoretical_p *= (365 - i) / 365
            
        theoretical_p = 1 - theoretical_p
        
        print(f"\n理论概率:{theoretical_p:.4f} ({theoretical_p*100:.2f}%)")
        
    # 分析M,N,P的关系
    print("\n分析:")
    print(f"1. 当N增大时，P会随之增加")
    print(f"2. 当M增大时，概率估计P会更加稳定和准确")
    print(f"3. 当N=23时，理论概率约为50.7%")
    print(f"4. 当N=57时，理论概率约为99%")
    
if __name__ == '__main__':
    main()