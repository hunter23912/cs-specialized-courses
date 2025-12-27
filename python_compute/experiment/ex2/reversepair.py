"""Reversed pair
revised from
Think Python by Allen B. Downey
http://thinkpython.com
"""

from bisect import bisect_left

# 默认是有序的
def make_word_list():
    """Reads lines from a file and builds a list using append."""
    word_list = []
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        word_list.append(word)
    return word_list

# 二分方法，优于列表O(n)查找，时间复杂度为O(logn),劣于集合方法O(1)
def in_bisect(word_list, word):
    """Checks whether a word is in a list using bisection search.

    Precondition: the words in the list are sorted

    word_list: list of strings
    word: string
    """
    
    # 如果word在word_list中，返回第一次出现的位置
    # 如果word不在word_list中，返回word应该插入的位置
    i = bisect_left(word_list, word)
    if i != len(word_list) and word_list[i] == word:
        return True
    else:
        return False

def reverse_pair(word_list, word):
    """Checks whether a reversed word appears in word_list.

    word_list: list of strings
    word: string
    """
    rev_word = word[::-1]
    return in_bisect(word_list, rev_word)       

if __name__ == '__main__':
    word_list = make_word_list()
    
    for word in word_list:
        if reverse_pair(word_list, word):
            print(word, word[::-1])


