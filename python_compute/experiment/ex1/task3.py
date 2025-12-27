import os, time
from pprint import pprint

# 定义装饰器
def timecal(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}运行时间: {(end_time - start_time) * 1000}ms')
        return result
    return wrapper

# 判断反序
@timecal # 计算函数运行时间
def find_reverse_pairs(words):
    reverse_pairs = []
    word_set = set(words) # 将单词列表转换为集合，提高查找效率
    
    for word in words:
        reversed_word = word[::-1] # 字符串反转
        
        # 如果反转后的单词在集合中，且不等于原单词，则找到一个反转对
        if reversed_word in word_set and word != reversed_word:
            reverse_pairs.append((word, reversed_word))
            
            # 从集合中删除这两个单词，避免重复筛选
            word_set.remove(word)
            word_set.remove(reversed_word)
    return reverse_pairs

# 判断回文
@timecal # 计算函数运行时间
def is_reversed_word(words):
    reversed_words = []
    for word in words:
        reversed_word = word[::-1]
        if reversed_word == word:
            reversed_words.append(word)
    return reversed_words

# 读取文件中的单词,按行分割
def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words 


def main():
# 读取文件中的单词
    words = read_words_from_file('./Python计算实验一/words.txt')

    # 寻找反序对
    reverse_pairs= find_reverse_pairs(words)
    pprint(reverse_pairs)
    
    # 寻找回文单词
    huiwei_words = is_reversed_word(words)
    pprint(huiwei_words)
main()

