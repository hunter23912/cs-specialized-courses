# 编写时间类
class Time:
    def __init__(self, hourr=0, minute=0,second=0):
        self.hour = hourr
        self.minute = minute
        self.second = second
    
    def __str__(self):
        return f'{self.hour:02}:{self.minute:02}:{self.second:02}'
    
    def __add__(self, other):
        if not isinstance(other, Time):
            raise TypeError('Type error: Can not add Time with non-Time object')
        seconds = self.time2int() + other.time2int()
        return Time.int2time(seconds)
    
    def time2int(self):
        return self.hour * 3600 + self.minute * 60 + self.second
    
    @staticmethod
    def int2time(seconds):
        '''
        将秒数转换为时间对象
        '''
        hour = seconds // 3600
        minute = (seconds % 3600) // 60
        second = seconds % 60
        return Time(hour, minute, second)
    
    def printtime(self):
        print(self)
    
    def isafter(self, other):
        return self.time2int() > other.time2int()
    
    # 作用是：
    def increment(self, seconds):
        if seconds < 0:
            raise ValueError('Seconds must be positive')
        total_seconds = self.time2int() + seconds
        return Time.int2time(total_seconds)
    
    def isvalid(self):
        if not (0 <= self.hour < 24):
            return False
        if not (0 <= self.minute < 60):
            return False
        if not (0 <= self.second < 60):
            return False
        return True
    
if __name__ == '__main__':
    t1 = Time(10, 30, 15)
    t2 = Time(2, 45, 50)
    
    print("t1:", t1)
    print("t2:", t2)
    
    t3 = t1 + t2
    print("t1 + t2:", t3)
    
    print("t1 in seconds:", t1.time2int())
    print("t2 in seconds:", t2.time2int())
    
    print("打印时间1：", end='')
    t1.printtime()
    
    print('时间1是否在时间2之后：', t1.isafter(t2))
    
    t4 = t1.increment(5000)
    print("t1 + 5000 seconds:", t4)
    
    t5 = Time(25, 61, 61)
    print("t5 is valid:", t5.isvalid())