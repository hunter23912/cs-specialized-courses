import time
import redis
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# 设置matplotlib中文字体，
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Redis连接，创建redis连接对象，连接到本地redis服务，使用默认端口6379和数据库0
r = redis.Redis(host='localhost', port=6379, db=0)

# MySQL连接，创建mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="test"
) 
mycursor = mydb.cursor() # 创建游标对象

# 创建MySQL测试表
def setup_mysql():
    try:
        # 先删除旧表
        mycursor.execute("DROP TABLE IF EXISTS performance_test")
        # 创建新表，包含主键id和数据data
        mycursor.execute("""
            CREATE TABLE performance_test (
                id VARCHAR(255) PRIMARY KEY,
                data VARCHAR(255)
            )
        """)
        print("MySQL测试表创建成功")
    except Exception as e:
        print(f"MySQL表创建失败: {e}")

# 清空Redis和MySQL测试数据
def cleanup():
    r.flushdb() # 清空Redis数据库
    mycursor.execute("DELETE FROM performance_test") # 清空MySQL表
    mydb.commit() # 提交事务
    print("测试数据已清空")

# 测试用例1: 单条插入操作
def test_single_insert(n=1000):
    results = {"redis": [], "mysql": []} # 字典记录Redis和MySQL的执行时间
    
    # Redis 单条插入测试
    start_time = time.time()
    for i in tqdm(range(n), desc="Redis单条插入", unit="条"):
        r.set(f"key:{i}", f"value:{i}") # set方法插入键值对
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 单条插入测试
    start_time = time.time()
    for i in tqdm(range(n), desc="MySQL单条插入", unit="条"):
        mycursor.execute("INSERT INTO performance_test (id, data) VALUES (%s, %s)", 
                        (f"key:{i}", f"value:{i}"))
    mydb.commit()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"单条插入测试完成 ({n}条数据)")
    return results

# 测试用例2: 单条查询操作
def test_single_get(n=1000):
    results = {"redis": [], "mysql": []}
    
    # 准备数据
    cleanup()
    for i in tqdm(range(n), desc="准备数据", unit="条"):
        r.set(f"key:{i}", f"value:{i}")
        mycursor.execute("INSERT INTO performance_test (id, data) VALUES (%s, %s)", 
                        (f"key:{i}", f"value:{i}"))
    mydb.commit()
    
    # Redis 单条查询测试
    start_time = time.time()
    for i in tqdm(range(n), desc="Redis单条查询", unit="条"):
        value = r.get(f"key:{i}")
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 单条查询测试
    start_time = time.time()
    for i in tqdm(range(n), desc="MySQL单条查询", unit="条"):
        mycursor.execute("SELECT data FROM performance_test WHERE id = %s", (f"key:{i}",))
        value = mycursor.fetchone()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"单条查询测试完成 ({n}条数据)")
    return results

# 测试用例3: 单条更新操作
def test_single_update(n=1000):
    results = {"redis": [], "mysql": []}
    
    # 准备数据
    cleanup()
    for i in tqdm(range(n), desc="准备数据", unit="条"):
        r.set(f"key:{i}", f"value:{i}")
        mycursor.execute("INSERT INTO performance_test (id, data) VALUES (%s, %s)", 
                        (f"key:{i}", f"value:{i}"))
    mydb.commit()
    
    # Redis 单条更新测试
    start_time = time.time()
    for i in tqdm(range(n), desc="Redis单条更新", unit="条"):
        r.set(f"key:{i}", f"new_value:{i}")
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 单条更新测试
    start_time = time.time()
    for i in tqdm(range(n), desc="MySQL单条更新", unit="条"):
        mycursor.execute("UPDATE performance_test SET data = %s WHERE id = %s", 
                        (f"new_value:{i}", f"key:{i}"))
    mydb.commit()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"单条更新测试完成 ({n}条数据)")
    return results

# 测试用例4: 单条删除操作
def test_single_delete(n=1000):
    results = {"redis": [], "mysql": []}
    
    # 准备数据
    cleanup()
    for i in tqdm(range(n), desc="准备数据", unit="条"):
        r.set(f"key:{i}", f"value:{i}")
        mycursor.execute("INSERT INTO performance_test (id, data) VALUES (%s, %s)", 
                        (f"key:{i}", f"value:{i}"))
    mydb.commit()
    
    # Redis 单条删除测试
    start_time = time.time()
    for i in tqdm(range(n), desc="Redis单条删除", unit="条"):
        r.delete(f"key:{i}")
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 单条删除测试
    start_time = time.time()
    for i in tqdm(range(n), desc="MySQL单条删除", unit="条"):
        mycursor.execute("DELETE FROM performance_test WHERE id = %s", (f"key:{i}",))
    mydb.commit()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"单条删除测试完成 ({n}条数据)")
    return results

# 测试用例5: 批量操作
def test_batch_operations(n=10000):
    results = {"redis": [], "mysql": []}
    batch_size = 100
    
    # Redis 批量插入测试 (pipeline)
    start_time = time.time()
    pipe = r.pipeline() # redis的批量操作使用pipeline
    for i in tqdm(range(n), desc="Redis批量插入", unit="条"):
        pipe.set(f"batch:key:{i}", f"value:{i}")
        if (i + 1) % batch_size == 0:
            pipe.execute()
            pipe = r.pipeline()
    if n % batch_size != 0:
        pipe.execute()
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 批量插入测试
    start_time = time.time()
    values = []
    for i in tqdm(range(n), desc="MySQL批量插入", unit="条"):
        values.append((f"batch:key:{i}", f"value:{i}"))
        if (i + 1) % batch_size == 0:
            # mysql中使用executemany批量操作
            mycursor.executemany("INSERT INTO performance_test (id, data) VALUES (%s, %s)", values)
            mydb.commit()
            values = []
    if values:
        mycursor.executemany("INSERT INTO performance_test (id, data) VALUES (%s, %s)", values)
        mydb.commit()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"批量操作测试完成 ({n}条数据，批量大小={batch_size})")
    return results

# 测试用例6: 不同数据量级的性能变化
def test_scaling_performance():
    data_sizes = [100, 1000, 10000, 50000, 100000]
    redis_times = []
    mysql_times = []
    
    for size in tqdm(data_sizes, desc="不同数据量级性能测试", unit="个数据量"):
        print(f"\n测试数据量: {size}")
        cleanup()
        
        # Redis 插入
        start_time = time.time()
        pipe = r.pipeline()
        for i in tqdm(range(size), desc="Redis插入", unit="条"):
            pipe.set(f"scale:key:{i}", f"value:{i}")
            if (i + 1) % 1000 == 0:
                pipe.execute()
                pipe = r.pipeline()
        if size % 1000 != 0:
            pipe.execute()
        end_time = time.time()
        redis_time = end_time - start_time
        redis_times.append(redis_time)
        
        # MySQL 插入
        start_time = time.time()
        values = []
        for i in tqdm(range(size), desc="MySQL插入", unit="条"):
            values.append((f"scale:key:{i}", f"value:{i}"))
            if (i + 1) % 1000 == 0:
                mycursor.executemany("INSERT INTO performance_test (id, data) VALUES (%s, %s)", values)
                mydb.commit()
                values = []
        if values:
            mycursor.executemany("INSERT INTO performance_test (id, data) VALUES (%s, %s)", values)
            mydb.commit()
        end_time = time.time()
        mysql_time = end_time - start_time
        mysql_times.append(mysql_time)
        
        print(f"Redis耗时: {redis_time:.2f}秒")
        print(f"MySQL耗时: {mysql_time:.2f}秒")
    
    return data_sizes, redis_times, mysql_times

# 测试用例7: 随机查询性能
def test_random_access(n=1000, queries=500):
    results = {"redis": [], "mysql": []}
    
    # 准备数据
    cleanup()
    for i in tqdm(range(n), desc="准备数据", unit="条"):
        r.set(f"random:key:{i}", f"value:{i}")
        mycursor.execute("INSERT INTO performance_test (id, data) VALUES (%s, %s)", 
                       (f"random:key:{i}", f"value:{i}"))
    mydb.commit()
    
    # 生成随机查询索引
    import random
    indices = [random.randint(0, n-1) for _ in tqdm(range(queries), desc="生成随机索引", unit="条")]
    
    # Redis 随机查询测试
    start_time = time.time()
    for i in tqdm(indices, desc="Redis随机查询", unit="条"):
        value = r.get(f"random:key:{i}")
    end_time = time.time()
    results["redis"].append(end_time - start_time)
    
    # MySQL 随机查询测试
    start_time = time.time()
    for i in tqdm(indices, desc="MySQL随机查询", unit="条"):
        mycursor.execute("SELECT data FROM performance_test WHERE id = %s", (f"random:key:{i}",))
        value = mycursor.fetchone()
    end_time = time.time()
    results["mysql"].append(end_time - start_time)
    
    print(f"随机访问测试完成 ({n}条数据中随机查询{queries}次)")
    return results

# 绘制测试结果图表
def plot_results(data_sizes, redis_times, mysql_times):
    plt.figure(figsize=(15, 10))
    
    # 1. 不同数据量级的性能对比
    plt.subplot(2, 2, 1)
    plt.plot(data_sizes, redis_times, 'r-o', label='Redis')
    plt.plot(data_sizes, mysql_times, 'b-o', label='MySQL')
    plt.xlabel('数据量')
    plt.ylabel('执行时间 (秒)')
    plt.title('不同数据量级下的插入性能')
    plt.legend()
    plt.grid(True)
    
    # 2. 各种操作类型对比柱状图
    plt.subplot(2, 2, 2)
    operations = ['插入', '查询', '更新', '删除', '批量']
    
    # 收集各操作结果
    redis_results = []
    mysql_results = []
    
    # 单条插入 (1000条)
    insert_results = test_single_insert(1000)
    redis_results.append(insert_results["redis"][0])
    mysql_results.append(insert_results["mysql"][0])
    
    # 单条查询 (1000条)
    get_results = test_single_get(1000)
    redis_results.append(get_results["redis"][0])
    mysql_results.append(get_results["mysql"][0])
    
    # 单条更新 (1000条)
    update_results = test_single_update(1000)
    redis_results.append(update_results["redis"][0])
    mysql_results.append(update_results["mysql"][0])
    
    # 单条删除 (1000条)
    delete_results = test_single_delete(1000)
    redis_results.append(delete_results["redis"][0])
    mysql_results.append(delete_results["mysql"][0])
    
    # 批量操作 (10000条)
    batch_results = test_batch_operations(10000)
    redis_results.append(batch_results["redis"][0])
    mysql_results.append(batch_results["mysql"][0])
    
    x = np.arange(len(operations))  # x轴位置
    width = 0.35  # 柱宽
    
    plt.bar(x - width/2, redis_results, width, label='Redis')
    plt.bar(x + width/2, mysql_results, width, label='MySQL')
    
    plt.xlabel('操作类型')
    plt.ylabel('执行时间 (秒)')
    plt.title('不同操作的性能对比')
    plt.xticks(x, operations)
    plt.legend()
    
    # 3. 随机访问性能
    plt.subplot(2, 2, 3)
    random_results = test_random_access(10000, 1000)
    db_names = ['Redis', 'MySQL']
    plt.bar(db_names, [random_results["redis"][0], random_results["mysql"][0]])
    plt.xlabel('数据库')
    plt.ylabel('执行时间 (秒)')
    plt.title('随机访问性能 (1000次查询)')
    
    # 4. 性能比率图
    plt.subplot(2, 2, 4)
    ratios = [mysql/redis if redis > 0 else 0 for mysql, redis in zip(mysql_results, redis_results)]
    plt.bar(operations, ratios)
    plt.axhline(y=1, color='r', linestyle='-', alpha=0.3)
    plt.xlabel('操作类型')
    plt.ylabel('MySQL/Redis 时间比率')
    plt.title('MySQL与Redis性能比率')
    
    plt.tight_layout()
    plt.savefig('redis_vs_mysql_performance.svg')
    plt.show()

# 主测试流程
def run_tests():
    print("开始Redis与MySQL性能对比测试...")
    setup_mysql()
    
    # 运行不同数据量级的测试
    data_sizes, redis_times, mysql_times = test_scaling_performance()
    
    # 绘制结果图表
    plot_results(data_sizes, redis_times, mysql_times)
    
    # 清理
    cleanup()
    print("\n测试完成! 结果已保存")

if __name__ == "__main__":
    run_tests()