
def get_time_after_one_second(hour, minute, second):
    # 增加一秒
    second += 1
    # 如果秒数超过59，增加一分钟并重置秒数
    if second > 59:
        second = 0
        minute += 1
    # 如果分钟数超过59，增加一小时并重置分钟数
    if minute > 59:
        minute = 0
        hour += 1
    # 如果小时数超过23，重置为0
    if hour > 23:
        hour = 0
    return hour, minute, second


# 输入字符串存入input_time
input_time = input("请输入时间（格式：HH MM SS）：")
try:
    # 处理字符串，转换为整数
    hour, minute, second = map(int, input_time.split())
    # 计算一秒后的时间
    new_hour, new_minute, new_second = get_time_after_one_second(hour, minute, second)
    # 输出结果
    print(f"1秒后的时间是：{new_hour:02d} {new_minute:02d} {new_second:02d}")
except ValueError:
    print("输入格式错误，请按照HH MM SS的格式输入时间。")
