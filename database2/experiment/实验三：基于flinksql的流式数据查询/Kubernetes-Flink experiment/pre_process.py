import pandas as pd
import pyarrow.parquet as pq
import time
input_file = "large_relation"
output_file = "large_relation.csv"
dict_file = "dict.csv"
result_file = "task-0"
# def transform_to_parquet():
#     # 读取数据
#     df = pd.read_csv(input_file, sep=" ", header=None, names=["referrer", "referree"], dtype={"referrer": "int64", "referree": "int64"})

#     # 保存为 Parquet 格式
#     df.to_parquet(output_file, index=False)

#     print(f"写入 {output_file} 完成，行数：{len(df)}")

def transform_dict():
    # 1. 读取数据
    df = pd.read_csv(input_file, sep=" ", header=None, names=["referrer", "referree"])

    # 3. 对 referrer 列做字典映射
    referrer_ids, referrer_uniques = pd.factorize(df["referrer"], sort=True)
    df["referrer_id"] = referrer_ids.astype("int64") # 新的列referrer_id

    # 4. 对 referree 列做字典映射
    referree_ids, referree_uniques = pd.factorize(df["referree"], sort=True)
    df["referree_id"] = referree_ids.astype("int64") # 新的列referree_id

    # 5. 保存映射表(可选：仅在需要反查原值时才保存)
    # 将每一列的唯一值和其ID对应关系存起来
    pd.DataFrame({
        "referrer_value": referrer_uniques,
        "referrer_id": range(len(referrer_uniques))
    }).to_csv("referrer_" + dict_file, index=False)

    pd.DataFrame({
        "referree_value": referree_uniques,
        "referree_id": range(len(referree_uniques))
    }).to_csv("referree_" + dict_file, index=False)

    # 6. 在 DataFrame 中去掉原大整数列，只保留映射后的 ID 列
    df = df.drop(columns=["referrer","referree"])

    # 7. 保存为 Parquet 格式
    df.to_parquet(output_file, index=False)

    print(f"字典映射后写入 {output_file} 完成，行数：{len(df)}")

# ...existing code...

def transform_dict_to_csv():
    # 1. 读取数据
    df = pd.read_csv(input_file, sep=" ", header=None, names=["referrer", "referree"])

    # 2. 对 referrer 列做字典映射
    referrer_ids, referrer_uniques = pd.factorize(df["referrer"], sort=True)
    df["referrer_id"] = referrer_ids.astype("int64") # 新的列referrer_id

    # 3. 对 referree 列做字典映射
    referree_ids, referree_uniques = pd.factorize(df["referree"], sort=True)
    df["referree_id"] = referree_ids.astype("int64") # 新的列referree_id

    # 4. 保存映射表(可选：仅在需要反查原值时才保存)
    pd.DataFrame({
        "referrer_value": referrer_uniques,
        "referrer_id": range(len(referrer_uniques))
    }).to_csv("referrer_" + dict_file, index=False)

    pd.DataFrame({
        "referree_value": referree_uniques,
        "referree_id": range(len(referree_uniques))
    }).to_csv("referree_" + dict_file, index=False)

    # 5. 在 DataFrame 中去掉原大整数列，只保留映射后的 ID 列
    df = df.drop(columns=["referrer","referree"])
    
    # 6. 重命名列以符合 Flink 读取预期
    df = df.rename(columns={"referrer_id": "referrer", "referree_id": "referree"})

    # 7. 保存为 CSV 格式，不包含标题行，用空格分隔
    df.to_csv(output_file, sep=",", index=False, header=False)

    print(f"字典映射后写入 {output_file} 完成，行数：{len(df)}")

def retransform_dict():
    start_time = time.time()
    
    result_df = pd.read_csv(result_file, sep=",", header=None, names=["web1_id", "web2_id","similarity"])
    print(result_df.head(20))
    # exit(0)
    referr_dict = pd.read_csv('large_referrer_dict.csv')
    # ID->原值
    id_to_value = dict(zip(referr_dict["referrer_id"], referr_dict["referrer_value"]))
    
    # 还原web1和web2列
    result_df['web1'] = result_df['web1_id'].map(id_to_value)
    result_df['web2'] = result_df['web2_id'].map(id_to_value)
    # 删除ID列
    result_df = result_df[['web1', 'web2', 'similarity']]
    
    # 输出前20行
    print(result_df.head(20))
    
    # 保存为CSV文件
    result_df.to_csv("result_final.csv", index=False)
    end_time = time.time()
    cost_time = end_time - start_time
    print(f"转换为 CSV 格式完成，耗时：{cost_time:.2f}秒")
    
def show_parquet():
    # 打开Parquet文件
    table = pq.read_table(output_file)
    # 获取列名
    # column_names = table.schema.names
    
    # 读取数据为pandas的DataFrame对象
    df = table.to_pandas().head(10)
    print(df)

# 172.22.122.180
if __name__ == "__main__":
    # transform_dict_to_csv()
    # show_parquet()
    retransform_dict()