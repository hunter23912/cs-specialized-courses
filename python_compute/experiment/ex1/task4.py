from pprint import pprint
import re
from collections import Counter

# 返回字典，每个单词及其出现的频次
def count_words(file_path, keywords = None):
    with open(file_path, 'r') as file:
        # 读取文件内容，并使用正则表达式分割单词
        words = re.findall(r'\b\w+\b', file.read().lower())
        
        result = {}
        if keywords:
           # 统计关键词出现的次数
            keyword_counts = Counter(word for word in words if word in keywords)
        
            # 计算频率
            total_keywords = sum(keyword_counts.values())
            result = {word: count / total_keywords for word, count in keyword_counts.items()} 
        else:
        # 使用Counter统计单词出现的次数
            result = Counter(words)
    return result
# 测试用例
def test():
    test_file_path = 'demo4.txt'
    keywords = ['hello', 'python']
    result = count_words(test_file_path, keywords)
    pprint(result) 
# 运行测试用例
test()
