from tqdm import tqdm
import random
import re
from collections import defaultdict
from my_timer import timer

@timer
def markov_analysis(text, n, type='tuple'):
    '''
    实现n阶马尔可夫文本分析
    :param text: 输入文本
    :param n: 马尔可夫阶数
    :return: n阶马尔可夫模型的字典
    '''
    
    words = re.findall(r'\b\w+\b|[.!?]',text) # 提取单词和标点符号
    print("提取的单词和标点符号数量：", len(words))
    markov_dict = defaultdict(list) 
    
    # 提取前缀和后缀
    for i in tqdm(range(len(words) - n), desc='分析进度', unit='个'):
        if type == 'tuple':
            prefix = tuple(words[i:i+n])
        elif type == 'str':
            prefix = ''.join(words[i:i+n])
        elif type == 'list':
            prefix = words[i:i+n]
        else:
            raise ValueError("type参数只能为'tuple'、'str'或'list'")
        
        prefix = tuple(words[i:i+n]) # 前缀
        suffix = words[i+n]
        markov_dict[prefix].append(suffix)
    
    # 打印前10个前缀和后缀
    print("前10个前缀和后缀：")
    for i, (prefix, suffixes) in enumerate(list(markov_dict.items())[:10]):
        print(f"{i+1}: {prefix} -> {suffixes}")
        
    return markov_dict

@timer
def generate_text(markov_dict, n, count):
    '''
    根据马尔可夫分析结果生成随机文本
    :param markov_dict: 马尔可夫模型字典
    :param n: 马尔可夫阶数
    :param count: 生成的句子数量
    :return: 生成的文本
    '''
    sentence = []
    for _ in tqdm(range(count), desc='生成进度', unit='个'):
        # 随机选择一个前缀最为起点
        curprefix = random.choice(list(markov_dict.keys()))
        curword = list(curprefix)
        
        while True:
            suffixes = markov_dict.get(curprefix, [])
            
            if not suffixes:
                break
            
            # 随机选择一个后缀并添加到句子中
            next_word = random.choice(suffixes)
            curword.append(next_word)
            
            # 如果遇到句子结束符，则停止生成
            if next_word in ['.', '!', '?']:
                break
            
            # 更新当前生成的句子的前缀
            curprefix = tuple(curword[-n:]) 
            
        # 首字母大写，句子结尾加空格
        curword[0] = curword[0].capitalize()
        sentence.append(' '.join(curword))
    
    return ' '.join(sentence)

if __name__ == '__main__':
    # 读取文本文件
    with open('emma.txt','r',encoding='utf-8') as f:
        text = f.read()
    
    print("文本长度：", len(text))
    # print("文本内容：", text[:100])
    
    n = 5 # 马尔可夫阶数
    count = 3
    
    # 进行马尔可夫分析
    markov_dict = markov_analysis(text, n, type='str')
    
    # 生成随机文本
    result = generate_text(markov_dict, n, count)
    print("生成的随机文本：")
    print(result)
    

        