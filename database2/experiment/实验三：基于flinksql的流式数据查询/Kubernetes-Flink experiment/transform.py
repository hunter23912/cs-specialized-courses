import pandas as pd
import time
import os
from multiprocessing import Pool, cpu_count

output_file = "large_result_final.csv"
input_file = "all_tasks.csv"
temp_dir = "temp_chunks"  # 临时文件目录

def process_chunk(chunk_data, id_to_value, chunk_num):
    """处理单个数据块并保存为临时文件"""
    try:
        # 还原web1和web2列
        chunk_data['web1'] = chunk_data['web1_id'].map(id_to_value)
        chunk_data['web2'] = chunk_data['web2_id'].map(id_to_value)
        # 删除ID列
        chunk_data = chunk_data[["web1", "web2", "similarity"]]
        
        # 保存临时文件
        temp_file = os.path.join(temp_dir, f"chunk_{chunk_num}.csv")
        chunk_data.to_csv(temp_file, index=False)
        return chunk_num, len(chunk_data), temp_file
    except Exception as e:
        print(f"Error processing chunk {chunk_num}: {e}")
        return chunk_num, 0, None

def retransform_dict():
    start_time = time.time()
    
    # 创建临时目录
    os.makedirs(temp_dir, exist_ok=True)
    
    # 读取映射字典
    print("Reading reference dictionary...")
    referr_dict = pd.read_csv('large_referrer_dict.csv')
    id_to_value = dict(zip(referr_dict["referrer_id"], referr_dict["referrer_value"]))
    
    # 获取CPU核心数
    num_processes = cpu_count()
    print(f"Using {num_processes} processes for parallel processing")
    
    # 分块读取数据并并行处理
    print("Processing data chunks...")
    chunk_size = 10000000  
    processed_chunks = []
    
    with Pool(processes=num_processes) as pool:
        results = []
        chunk_num = 0
        
        # 读取数据并提交处理任务
        for chunk in pd.read_csv(input_file, sep=",", header=None, 
                                 names=["web1_id", "web2_id", "similarity"], 
                                 chunksize=chunk_size):
            results.append(pool.apply_async(process_chunk, 
                                           args=(chunk.copy(), id_to_value, chunk_num)))
            chunk_num += 1
        
        # 收集处理结果
        for result in results:
            processed_chunks.append(result.get())
    
    # 合并所有临时文件
    print("Merging temporary files...")
    first_chunk = True
    
    with open(output_file, 'w') as outfile:
        for chunk_num, chunk_size, temp_file in sorted(processed_chunks, key=lambda x: x[0]):
            if temp_file and os.path.exists(temp_file):
                with open(temp_file, 'r') as infile:
                    # 只写入第一个文件的头部
                    if first_chunk:
                        for line in infile:
                            outfile.write(line)
                        first_chunk = False
                    else:
                        # 跳过其他文件的头部
                        next(infile)
                        for line in infile:
                            outfile.write(line)
                # 删除临时文件
                os.remove(temp_file)
    
    # 删除临时目录
    os.rmdir(temp_dir)
    
    end_time = time.time()
    cost_time = end_time - start_time
    print(f"Success! Processed {sum(cs for _, cs, _ in processed_chunks)} rows in {cost_time:.2f}s")

if __name__ == "__main__":
    retransform_dict()