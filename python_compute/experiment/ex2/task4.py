from my_timer import *

# 加载单词文件，返回单词集合
def load_words(filename):
    with open(filename) as f:
        words = set(f.read().splitlines())
        print(f'已加载{len(words)}个单词')
    return words

def is_reducible(word, word_set, memo):
    '''
    判断单词是否可缩减
    :param word: 待判断单词
    :param word_set: 单词集合
    :param memo: 已找到的可缩减单词缓存
    :return: 返回是否可缩减和缩减路径
    '''

    # 如果单词已经在缓存中，直接返回结果
    if word in memo:
        return memo[word]
    
    # 终结情况：空字符串和a,i
    if word == '' or (len(word) == 1 and word in {'a', 'i'}):
        memo[word] = (True, [word])
        return memo[word]

    # 生成所有可能的子单词(删除一个字母)
    children = [word[:i] + word[i+1:] for i in range(len(word))]
    
    # 检查每个子单词是否可缩减
    for child in children:
        if child in word_set:
            reducible, path = is_reducible(child, word_set, memo) # 递归入口
            if reducible:
                # 缓存结果
                memo[word] = (True, [word] + path)
                print(f'找到可缩减单词：{word} (长度：{len(word)})')
                return memo[word]
    
    # 未找到可缩减路径
    memo[word] = (False, [])
    return memo[word]

@timer
def find_longest_reducible(word_set):
    '''
    查找最长的可缩减单词
    :param word_set: 单词集合
    :return: 返回(最长可缩减单词,缩减路径)
    '''
    memo = {} # 缓存已找到的可缩减单词
    longest = []
    longest = ('', []) # 最长可缩减单词和路径
    
    # 按照单词长度降序排列所有单词(能以最快速度找到单词)
    sorted_words = sorted(word_set, key=lambda x: len(x), reverse=True)
    
    
    for word in sorted_words:
        # 如果当前单词比已找到的最长短，提前终止
        if len(word) < len(longest[0]):
            break
        
        # 传入当前单词，单词集合，和缓存字典
        reducible, path = is_reducible(word, word_set, memo) # 判断单词是否可缩减，返回bool结果和路径
        if reducible and len(word) > len(longest[0]):
            longest = (word, path)
            # print(type(word),type(path))
            print(f'找到新的最长可缩减单词：{word} (长度：{len(word)})')
    return longest

def main():
    # 加载单词文件
    word_set = load_words('words.txt')
    
    # 添加空字符串到单词集合(作为递归基准)
    word_set.add('')
    word_set.add('a')
    word_set.add('i')
    
    # 查找最长可缩减单词
    longest_word, path = find_longest_reducible(word_set)
    
    # 输出结果
    if longest_word:
        print(f'最长可缩减单词为：{longest_word} (长度： {len(longest_word)})')
        # for word, path in longest_word:
            # print(f'单词：{word} (长度：{len(word)})，缩减路径：{"->".join(path)}')
        print(f'缩减路径：{'->'.join(path)}')
    else:
        print('没有找到可缩减单词')
    
if __name__ == '__main__':
    main()