import time
from functools import wraps
def timer(func):
    '''
    装饰器，用于测试函数运行时间
    '''
    @wraps(func) # 保留原始函数的元信息（如名称、文档字符串等）
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter() # 更高精度的计时器
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = (end_time - start_time) * 1000 # 将时间转换为毫秒
        print(f"函数{func.__name__}的运行时间为：{run_time:.9f}ms") # func和wrapper的__name__经过装饰后，应该是一样的
        return result
    return wrapper
        