# 对PL0程序进行词法分析
keywords = {
    'const' : 'constsym',
    'var' : 'varsym',
    'procedure' : 'proceduresym',
    'begin' : 'beginsym',
    'end' : 'endsym',
    'if' : 'ifsym',
    'then' : 'thensym',
    'while' : 'whilesym',
    'do' : 'dosym',
    'call' : 'callsym',
    'write' : 'writesym',
    'odd' : 'oddsym',
}

# 词法分析器
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
    
    # 移动到下一个字符，如果到达文本末尾，则设置当前字符为None
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    # 跳过空白字符
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    # 识别标识符或关键字
    def _id(self):
        result = ''
        
        # 循环读取字母或数字，直到遇到非法字符
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
            result += self.current_char.lower() # 统一转换为小写
            self.advance()
        # 判断是否为关键字
        return (keywords[result], result) if result in keywords else ('ident' , result) # 返回的是一个元组
    
    # 识别数字常量
    def _number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        # 检查数字后是否跟字母，如果是则报错
        if self.current_char and self.current_char.isalpha():
            raise Exception(f'Invalid number at position {self.pos}')
        return ('number', int(result))
    
    # 从输入文本提取下一个单词符号,返回一个元组
    def get_next_token(self):
        while self.current_char is not None:
            # 跳过空白字符
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 识别标识符或关键字
            if self.current_char.isalpha():
                return self._id()
            
            # 识别数字常量
            if self.current_char.isdigit():
                return self._number()
            
            # 处理多字符运算符
            next_char = self.text[self.pos + 1] if self.pos + 1 < len(self.text) else ''
            
            if self.current_char == ':':
                if next_char == '=': # 检测:=
                    self.advance()
                    self.advance()
                    return ('become', ':=')
                else:
                    raise Exception(f"Unexpected character ':' at position {self.pos}")
                
            if self.current_char == '<':
                self.advance()
                if next_char == '=':
                    self.advance()
                    return ('leq' , '<=')
                elif next_char == '>':
                    self.advance()
                    return ('neq' , '<>')
                return ('lss' , '<')
            
            if self.current_char == '>':
                self.advance()
                if next_char == '=':
                    self.advance()
                    return ('geq' , '>=')
                return ('gtr' , '>')
            
            # 处理单字符运算符
            if self.current_char == '+':
                self.advance()
                return ('plus', '+')
            if self.current_char == '-':
                self.advance()
                return ('minus', '-')
            if self.current_char == '*':
                self.advance()
                return ('times', '*')
            if self.current_char == '/':
                self.advance()
                return ('slash', '/')
            if self.current_char == '=':
                self.advance()
                return ('eql', '=')
            if self.current_char == ';':
                self.advance()
                return ('semicolon', ';')
            if self.current_char == ',':
                self.advance()
                return ('comma', ',')
            if self.current_char == '(':
                self.advance()
                return ('lparen', '(')
            if self.current_char == ')':
                self.advance()
                return ('rparen', ')')
            if self.current_char == '.':
                self.advance()
                return ('period', '.')
            
            # 如果遇到未知字符，则抛出异常
            raise Exception(f"Uknown character ' {self.current_char}' at positon {self.pos}")
        
        # 如果到达文件结尾，则返回EOF
        return ('EOF', None)
    
# 主函数，执行词法分析
def main(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            text = f.read()
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token[0] == 'EOF':
                break
            
            tokens.append(f'({token[0]}, {token[1]})')
        
        # 将词法分析结果写入输出文件
        with open(output_file, 'w') as f:
            f.write('\n'.join(tokens))
        print(f"Lexical analysis completed. Output written to: {output_file}")
    except FileNotFoundError:
        # 如果输入文件不存在，抛出异常
        raise Exception(f"Error: The input file '{input_file}' was not found. Please check the file path.")

    except IOError as e:
        # 如果文件读取或写入过程中发生 I/O 错误，抛出异常
        raise Exception(f"Error: An I/O error occurred while processing the file. Details: {e}")

    except Exception as e:
        # 捕获其他未知异常，并打印详细信息
        raise Exception(f"An unexpected error occurred: {e}")
        
                
if __name__ == '__main__':
    main('input.txt', 'output.txt')
