'''
这是一个学习使用redis的示例代码
使用redis的基本操作
'''
import redis, time, json
from datetime import datetime

def main():
    # 连接到redis服务器
    r = redis.Redis(host='localhost', port=6379)
    try:
        print('测试redis连接:', r.ping())
        
        r.flushdb()  # 清空数据库
        print('=== redis 数据库已清空 ===')
        
        print('=== 字符串操作 ===')
        r.set('name', '张三')
        print('设置name:', r.get('name').decode('utf-8'))
        
        name = r.get('name')
        print('获取name:', name.decode('utf-8'))
        
        # 设置键值对，过期时间
        r.setex('code', 10, '123456')
        print('设置 code=123456, 10秒后过期')
        
        # 获取并等待过期
        print(f'获取 code: {r.get('code').decode("utf-8")}')
        print('等待5秒')
        time.sleep(5)
        print('等待6秒')
        time.sleep(6)
        print(f'再过6秒后 code: {r.get("code")}')
        
        # 设置多个键值对
        r.mset({'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})
        print('设置多个键值对: key1=value1, key2=value2, key3=value3')
        
        # 获取多个键值对
        values = r.mget('key1', 'key2', 'key3')
        print(f'获取多个键值对: {values}')
        
        # 数值操作
        r.set('counter', 10)
        print('设置 counter=10')
        
        # 自增
        r.incr('counter')
        print(f'counter 自增 1: {r.get('counter')}')
        
        # 增加指定值
        r.incrby('counter', 5)
        print(f'counter 自增 5: {r.get("counter").decode("utf-8")}')
        
        # 自减
        r.decr('counter')
        print(f'counter 自减 1: {r.get("counter").decode("utf-8")}')
        
        # 减少指定值
        r.decrby("counter", 3)
        print(f"counter 自减 3: {r.get('counter')}")
        
        # 2. 列表操作 (List)
        print("\n=== 列表操作 ===")
        
        # 左侧推入元素
        r.lpush("languages", "Python", "Java", "C++")
        print("左侧推入: Python, Java, C++")
        
        # 右侧推入元素
        r.rpush("languages", "JavaScript", "Go")
        print("右侧推入: JavaScript, Go")
        
        # 获取列表长度
        length = r.llen("languages")
        print(f"列表长度: {length}")
        
        # 获取列表范围
        languages = r.lrange("languages", 0, -1)  # 全部元素
        print(f"列表所有元素: {languages}")
        
        # 左侧弹出元素
        left_item = r.lpop("languages")
        print(f"左侧弹出: {left_item}")
        
        # 右侧弹出元素
        right_item = r.rpop("languages")
        print(f"右侧弹出: {right_item}")
        
        # 获取更新后的列表
        languages = r.lrange("languages", 0, -1)
        print(f"更新后的列表: {languages}")
        
        # 3. 集合操作 (Set)
        print("\n=== 集合操作 ===")
        
        # 添加集合元素
        r.sadd("fruits", "apple", "banana", "cherry", "apple")  # 重复元素会被忽略
        print("添加到集合: apple, banana, cherry, apple(重复)")
        
        # 获取集合元素数量
        count = r.scard("fruits")
        print(f"集合元素数量: {count}")
        
        # 获取集合所有元素
        fruits = r.smembers("fruits")
        print(f"集合所有元素: {fruits}")
        
        # 检查元素是否在集合中
        is_member = r.sismember("fruits", "apple")
        print(f"apple 是否在集合中: {is_member}")
        
        # 删除集合元素
        r.srem("fruits", "banana")
        print("从集合中删除: banana")
        
        # 获取更新后的集合
        fruits = r.smembers("fruits")
        print(f"更新后的集合: {fruits}")
        
        # 集合运算
        r.sadd("vegetables", "carrot", "spinach", "cherry")
        print("创建新集合 vegetables: carrot, spinach, cherry")
        
        # 交集
        intersection = r.sinter("fruits", "vegetables")
        print(f"fruits 和 vegetables 的交集: {intersection}")
        
        # 并集
        union = r.sunion("fruits", "vegetables")
        print(f"fruits 和 vegetables 的并集: {union}")
        
        # 差集
        difference = r.sdiff("fruits", "vegetables")
        print(f"fruits 减去 vegetables 的差集: {difference}")
        
        # 4. 有序集合操作 (Sorted Set)
        print("\n=== 有序集合操作 ===")
        
        # 添加带分数的元素
        r.zadd("scores", {"Alice": 95, "Bob": 87, "Charlie": 92})
        print("添加到有序集合: Alice(95), Bob(87), Charlie(92)")
        
        # 获取元素分数
        score = r.zscore("scores", "Alice")
        print(f"Alice 的分数: {score}")
        
        # 增加元素分数
        r.zincrby("scores", 3, "Bob")
        print(f"给 Bob 加 3 分，新分数: {r.zscore('scores', 'Bob')}")
        
        # 获取排名
        rank = r.zrevrank("scores", "Bob")  # 按分数从高到低排序
        print(f"Bob 的排名(从高到低): {rank + 1}")  # rank 从 0 开始
        
        # 获取分数范围内的元素
        members = r.zrangebyscore("scores", 90, 100)
        print(f"分数在 90-100 之间的成员: {members}")
        
        # 获取所有成员及其分数
        result = r.zrange("scores", 0, -1, withscores=True)
        print("所有成员及分数:")
        for member, score in result:
            print(f"  {member}: {score}")
        
        # 5. 哈希表操作 (Hash)
        print("\n=== 哈希表操作 ===")
        
        # 设置哈希表字段
        r.hset("user:1", "name", "李四")
        r.hset("user:1", "age", 25)
        r.hset("user:1", "email", "lisi@example.com")
        print("创建哈希表 user:1: name=李四, age=25, email=lisi@example.com")
        
        # 批量设置哈希表字段
        r.hmset("user:2", {"name": "王五", "age": 30, "email": "wangwu@example.com"})
        print("创建哈希表 user:2: name=王五, age=30, email=wangwu@example.com")
        
        # 获取单个字段值
        name = r.hget("user:1", "name")
        print(f"user:1 的 name 字段: {name}")
        
        # 获取多个字段值
        info = r.hmget("user:1", "name", "age", "email")
        print(f"user:1 的多个字段: {info}")
        
        # 获取所有字段和值
        all_info = r.hgetall("user:1")
        print(f"user:1 的所有字段和值: {all_info}")
        
        # 检查字段是否存在
        exists = r.hexists("user:1", "phone")
        print(f"user:1 是否有 phone 字段: {exists}")
        
        # 删除字段
        r.hdel("user:1", "email")
        print("删除 user:1 的 email 字段")
        print(f"删除后的 user:1: {r.hgetall('user:1')}")
        
        # 6. 事务操作
        print("\n=== 事务操作 ===")
        
        # 开始事务
        pipe = r.pipeline(transaction=True)
        
        # 添加命令到事务
        pipe.set("transaction_key1", "value1")
        pipe.set("transaction_key2", "value2")
        pipe.incr("transaction_counter") 
        
        # 执行事务
        results = pipe.execute()
        print(f"事务执行结果: {results}")
        
        # 验证事务结果
        print(f"transaction_key1: {r.get('transaction_key1')}")
        print(f"transaction_key2: {r.get('transaction_key2')}")
        print(f"transaction_counter: {r.get('transaction_counter')}")
        
        # 7. 发布/订阅 (这部分通常在两个不同的程序中进行)
        print("\n=== 发布/订阅 ===")
        print("发布消息到频道 'channel1'")
        r.publish("channel1", f"这是一条测试消息，时间: {datetime.now()}")
        print("注意：订阅需要单独的程序或线程来处理，这里只展示发布")
        
        # 8. 键过期和持久化
        print("\n=== 键过期和持久化 ===")
        
        # 设置键的过期时间
        r.set("temp_key", "临时值")
        r.expire("temp_key", 30)  # 30秒后过期
        print("设置 temp_key 30秒后过期")
        
        # 获取键的剩余生存时间
        ttl = r.ttl("temp_key")
        print(f"temp_key 的剩余生存时间: {ttl} 秒")
        
        # 取消键的过期设置
        r.persist("temp_key")
        print("取消 temp_key 的过期设置")
        print(f"取消后的生存时间: {r.ttl('temp_key')} (-1 表示永久)")
        
        # 9. 使用 Redis 存储和读取 JSON 对象
        print("\n=== 使用 Redis 存储 JSON ===")
        
        # 创建 JSON 对象
        user_data = {
            "id": 12345,
            "name": "赵六",
            "profile": {
                "age": 28,
                "job": "软件工程师",
                "skills": ["Python", "Redis", "MongoDB"]
            },
            "active": True
        }
        
        # 将 JSON 对象序列化并存储
        r.set("user:json", json.dumps(user_data, ensure_ascii=False))
        print(f"将 JSON 对象存储到 Redis: {user_data}")
        
        # 读取并解析 JSON 对象
        stored_json = r.get("user:json")
        parsed_data = json.loads(stored_json)
        print(f"从 Redis 读取并解析 JSON 对象: {parsed_data}")
        print(f"用户技能: {parsed_data['profile']['skills']}")
        
        # 10. Redis 性能测试
        print("\n=== Redis 性能测试 ===")
        
        # 测试设置和获取字符串性能
        print("测试设置 10000 个键值对...")
        start_time = time.time()
        pipe = r.pipeline()
        for i in range(10000):
            pipe.set(f"test:{i}", f"value:{i}")
            if i % 1000 == 0:  # 每1000个操作执行一次
                pipe.execute()
                pipe = r.pipeline()
        pipe.execute()  # 执行剩余的操作
        end_time = time.time()
        print(f"设置 10000 个键值对耗时: {end_time - start_time:.4f} 秒")
        
        # 测试获取字符串性能
        print("测试获取 10000 个键值对...")
        start_time = time.time()
        pipe = r.pipeline()
        for i in range(10000):
            pipe.get(f"test:{i}")
            if i % 1000 == 0:  # 每1000个操作执行一次
                pipe.execute()
                pipe = r.pipeline()
        pipe.execute()  # 执行剩余的操作
        end_time = time.time()
        print(f"获取 10000 个键值对耗时: {end_time - start_time:.4f} 秒")
        
        print("=== 示例完成 ===")
    except redis.ConnectionError:
        print('无法连接到redis服务器,请检查服务器是否启动且可访问')
    except Exception as e:
        print(f'发生错误: {e}')
        return

if __name__ == '__main__':
    main()