import os, re, unittest
# from wordprocess import *

class Tasks:
    def rotateword(strsrc, n) -> str:
        '''
        将字符串中每个字母在字母表中轮转n个位置
        params:
            strsrc: 需要轮转的字符串
            n: 轮转位置
        return: 轮转后的字符串
        '''
        ans = ''
        for c in strsrc:
            if c.isalpha():
                # 确定字母大小写
                if c.isupper():
                    rotated = chr((ord(c) - ord('A') + n) % 26 + ord('A'))
                else:
                    rotated = chr((ord(c) - ord('a') + n) % 26 + ord('a'))
                ans += rotated
            else:
                ans += c
        return ans

    # 判断word中是否没有str中的字母
    def avoids(word, str) -> bool:
        ''' 
        params:
            word: 需要检查的单词
            str: 需要避免的字母
        return:
            True: 如果word中没有str中的字母
            False: 如果word中有str中的字母
        '''
        # ban_word是str,包含了需要避免的字母
        ban_word = f'[{re.escape(str)}]'
        if(re.search(ban_word, word)):
            return False
        return True

    # 判断word中是否只有str中的字母
    def useonly(word, allowed) -> bool:
        '''
        params:
            word: 需要检查的单词
            allowed: 允许的字母
        return:
            True: 如果word中只有allowed中的字母
            False: 如果word中有不在allowed中的字母
        '''
        # ^表示取反，allowed_word是str,包含了需要允许的字母
        not_allowed_word = f'[^{re.escape(allowed)}]'
        
        if re.search(not_allowed_word, word):
            return False
        return True

    # 判断word中是否有str中所有字母各至少一个
    def useall(word, str) -> bool:
        '''
        params:
            word: 需要检查的单词
            str: 需要使用的字母
        return:
            True: 如果word中有str中所有字母各至少一个
            False: 否则
        '''
        # use_word是str,包含了需要使用的字母
        for c in str:
            if c not in word:
                return False
        return True
    
    def find_all_aeiou(filename = 'words.txt') -> list:
        '''
        从文件中读取单词，返回包含所有元音字母的单词列表
        params:
            filename: 文件名
        return: 包含所有元音字母的单词列表
        '''
        target = 'aeiou'
        result = []
        try:
            with open(filename, 'r') as f:
                for word in f:
                    word = word.strip()
                    if Tasks.useall(word, target):
                        result.append(word)
            return result
        except FileNotFoundError:
            print(f'文件{filename}不存在')
            return []
    
    # 判断单词是否含有e
    def hasnoe(word) -> bool:
        '''
        判断单词是否含有e
        params:
            word: 需要检查的单词
        return:
            True: 单词中无e
        '''
        return 'e' not in word.lower()

    def cal_noe(filename = 'words.txt') -> float:
        '''
        计算不含e的单词在整个列表中的占比
        return: 
            不含e的单词在整个列表中的占比
        '''
        try:
            total = 0
            noe = 0
            with open(filename, 'r') as f:
                for line in f:
                    total += 1
                    if Tasks.hasnoe(line):
                        noe += 1
            if total == 0:
                return 0
            
            ans = round(noe / total, 5)
            return ans
        except FileNotFoundError:
            print(f'文件{filename}不存在')
            return 0
    
    # 判断单词是否是字母顺序排列的
    def isabecedarian(word) -> bool:
        '''
        判断单词是否是字母顺序排列的
        params:
            word: 需要检查的单词
        return:
            True: 单词是字母顺序排列的
            False: 单词不是字母顺序排列的
        '''
        word = word.lower()
        for i in range(len(word) - 1):
            if word[i] > word[i + 1]:
                return False
        return True

    def find_all_abecedarian(filename = 'words.txt') -> list:
        '''
        从文件中读取单词，返回字母顺序排列的单词列表
        params:
            filename: 文件名
        return: 字母顺序排列的单词列表
        '''
        result = []
        try:
            with open(filename, 'r') as f:
                for word in f:
                    word = word.strip()
                    if Tasks.isabecedarian(word):
                        result.append(word)
            print('文件大小：', os.path.getsize(filename), '字节')
            return result
        except FileNotFoundError:
            print(f'文件{filename}不存在')
            return []
        
class Test(Tasks):
    def test_rotateword(self):
        # 测试基本功能
        self.assertEqual(Tasks.rotateword("abc", 1), "bcd")
        self.assertEqual(Tasks.rotateword("xyz", 1), "yza")
        # 测试大写字母
        self.assertEqual(Tasks.rotateword("ABC", 1), "BCD")
        # 测试混合大小写
        self.assertEqual(Tasks.rotateword("aBcXyZ", 1), "bCdYzA")
        # 测试负数轮转
        self.assertEqual(Tasks.rotateword("abc", -1), "zab")
        # 测试非字母字符
        self.assertEqual(Tasks.rotateword("a1b!c", 1), "b1c!d")
    
    def test_avoids(self):
        self.assertTrue(Tasks.avoids("python", "xz"))
        self.assertFalse(Tasks.avoids("python", "p"))
        self.assertTrue(Tasks.avoids("hello", "xyz"))
        self.assertFalse(Tasks.avoids("hello", "lo"))
        
    def test_useonly(self):
        self.assertTrue(Tasks.useonly("abc", "abcdef"))
        self.assertFalse(Tasks.useonly("xyz", "abcdef"))
        self.assertTrue(Tasks.useonly("aabbcc", "abc"))
        self.assertFalse(Tasks.useonly("python", "pyth"))
        
    def test_useall(self):
        self.assertTrue(Tasks.useall("education", "aeiou"))
        self.assertFalse(Tasks.useall("python", "aeiou"))
        self.assertTrue(Tasks.useall("abcdef", "def"))
        self.assertFalse(Tasks.useall("hello", "xyz"))
        
    def test_hasnoe(self):
        self.assertTrue(Tasks.hasnoe("python"))
        self.assertFalse(Tasks.hasnoe("hello"))
        self.assertTrue(Tasks.hasnoe("coding"))
        self.assertFalse(Tasks.hasnoe("developer"))
        
    def test_isabecedarian(self):
        self.assertTrue(Tasks.isabecedarian("abcdef"))
        self.assertFalse(Tasks.isabecedarian("banana"))
        self.assertTrue(Tasks.isabecedarian("abhort"))
        self.assertTrue(Tasks.isabecedarian("a"))
        self.assertTrue(Tasks.isabecedarian(""))    

def main():
    # 检查words.txt文件是否存在，如果不存在则先创建示例文件
    
    filename = 'words.txt'
    if not os.path.exists(filename):
        print(f"文件 {filename} 不存在!")
        
    print("=== 单词处理函数测试 ===")
    
    # 测试rotateword:将每个字母向后移一位
    print("\n1. rotateword 函数测试:")
    test_word = "Hello"
    n = 1
    rotated = Tasks.rotateword(test_word, n)
    print(f"  原单词: {test_word}, 轮转{n}位后: {rotated}")
    
    # 测试avoids函数
    print("\n2. avoids 函数测试:")
    test_word = "programming"
    forbidden = "xyz"
    result = Tasks.avoids(test_word, forbidden)
    print(f"  单词 '{test_word}' 是否不包含禁止字母 '{forbidden}': {result}")
    
    # 测试useonly函数
    print("\n3. useonly 函数测试:")
    test_word = "aabbcc"
    allowed = "abc"
    result = Tasks.useonly(test_word, allowed)
    print(f"  单词 '{test_word}' 是否仅由允许字母 '{allowed}' 组成: {result}")

    # 测试useall函数
    print("\n4. useall 函数测试:")
    test_word = "education"
    required = "aeiou"
    result = Tasks.useall(test_word, required)
    print(f"  单词 '{test_word}' 是否包含所有字母 '{required}': {result}")
    # 找出words.txt中所有包含所有元音字母的单词
    aeiou_list = Tasks.find_all_aeiou(filename)
    print(f"  包含所有元音字母的单词列表:")
    for i in range(0,len(aeiou_list), 10):
        print(' '.join(aeiou_list[i:i+10]))
    
    # 测试hasnoe函数
    print("\n5. hasnoe 函数测试:")
    test_word = "python"
    result = Tasks.hasnoe(test_word)
    print(f"  单词 '{test_word}' 是否不包含字母 'e': {result}")
    # 求出words.txt中不含字母 'e' 的单词在列表中的占比
    neolist = Tasks.cal_noe(filename)
    print(f"  不含字母 'e' 的单词在列表中的占比: {neolist}")
    
    print("\n6. isabecedarian 函数测试:")
    test_word = "abcde"
    result = Tasks.isabecedarian(test_word)
    print(f"  单词 '{test_word}' 是否字母顺序排列: {result}")
    # 找出words.txt中所有字母顺序排列的单词
    abecedarian_list = Tasks.find_all_abecedarian(filename)
    print(f"  字母顺序排列的单词列表:")
    for i in range(0,len(abecedarian_list), 10):
        print(' '.join(abecedarian_list[i:i+10]))

if __name__ == "__main__":
    main()