# Ackerman函数递归实现
from my_timer import *
import random

def ackerman(m, n):
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackerman(m - 1, 1)
    elif m > 0 and n > 0:
        return ackerman(m - 1, ackerman(m, n - 1))
    
# 去重函数，保持顺序，使用set来存储唯一元素
def unique(items):
    '''
    return list, set
    '''
    unique = set()
    result = []
    for item in items:
        if item not in unique:
            unique.add(item)
            result.append(item)
    return result, unique

def test1():
    m = 4
    n = 3
    result = ackerman(m, n)
    print(f"Ackerman({m}, {n}) = {result}")

def test2():
    # 生成随机列表
    random_list = [random.randint(1, 10) for _ in range(20)]
    print("原始随机列表：",random_list)
    print("去重后的列表：",unique(random_list)[0])
    print("去重后的集合：",unique(random_list)[1])
    
    # 生成随机字典
    random_dict = {random.randint(1, 10): random.randint(1, 10) for _ in range(20)} 
    print("原始随机字典：",random_dict)
    
    # 对字典去重并保持顺序
    unique_values = unique(list(random_dict.values()))[0]
    print("去重后的字典值列表：", unique_values)
    
def main():
    # test2()
    ackerman(3,4)

if __name__ == "__main__":
    main()