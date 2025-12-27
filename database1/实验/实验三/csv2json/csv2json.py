import csv
import json

# CSV文件路径
csv_file_path = "../us_births_2016_2021.csv"
# 输出的JSON文件路径
json_file_path = "../us_births_2016_2021.json"

# 初始化一个列表来保存所有的字典记录
data = []

# 读取CSV文件
with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # 将CSV记录转换为JSON对象
        data.append(json.dumps(row))

# 将JSON对象列表写入JSON文件，每个对象占用一行
with open(json_file_path, mode="w", encoding="utf-8") as json_file:
    for json_obj in data:
        json_file.write(json_obj + "\n")
