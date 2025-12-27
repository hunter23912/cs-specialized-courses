import math
from my_timer import *
from decimal import Decimal, getcontext # 这两个库分别是用来处理浮点数的精度问题的

@timer
def calculate_pi():
    # 设置浮点数的精度为20位
    getcontext().prec = 20 
    
    sum_result = Decimal(0) # 用来存储最终的结果
    k = 0 
    while True:
        # 计算分子
        numerator = math.factorial(4 * k) * (1103 + 26390 * k)
        # 计算分母
        denominator = (math.factorial(k) ** 4) * (396 ** (4 * k))
        # 计算当前项
        term = Decimal(numerator) / Decimal(denominator)
        sum_result += term
        
        # 计算当前pi的近似值
        pi_approx = Decimal(9801) / (Decimal(2) * Decimal(2).sqrt() * sum_result)
        
        # 检查当前精度是否达到小数点后15位
        if k > 0:
            diff = abs(pi_approx - Decimal(math.pi))
            if diff < Decimal(1e-15):
                break
        k += 1
    return pi_approx

# 计算pi的近似值
pi_approx = calculate_pi()

print(f"计算得到的pi值：{pi_approx}")
print(f"math.pi的值：{Decimal(math.pi)}")
print(f"两者的差值：{abs(pi_approx - Decimal(math.pi))}")

    