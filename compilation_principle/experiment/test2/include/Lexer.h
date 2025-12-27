#ifndef LEXER_H
#define LEXER_H
#include <cstddef>

#include "Utils.h"

// 定义词法单元结构体，包含类型和值
struct Token {
    std::string type;   // 类型
    std::string value;  // 值
};

class Lexer {
private:
    std::string text;
    size_t pos;
    char current_char;
    std::unordered_map<std::string, std::string> keywords;
    size_t current_token_index;  // 当前Token索引
    Token current_token;         // 当前Token

    void advance();               // 移动到下一个字符
    void skip_whitespace();       // 跳过空白字符
    void skip_comment();          // 跳过注释
    Token _id();                  // 识别标识符或关键字
    Token _number();              // 识别数字常量
    Token _string();              // 识别字符串常量
    char peek_next() const;       // 获取下一个字符
    Token process_colon();        // 处理多字符运算符 “:=”
    Token process_less();         // 处理”<”和”<=”和”<>”
    Token process_greater();      // 处理”>”和”>=”
    Token process_single_char();  // 处理单字符运算符和分隔符
public:
    std::vector<Token> tokens;                         // 存储词法单元
    Lexer(const std::string &text);                    // 构造函数
    Token get_next_token();                            // 获取下一个词法单元
    void setTokens(const std::vector<Token> &tokens);  // 设置词法单元
    Token get_current_token() const;                   // 设置当前Token
    void advance_token();                              // 移动到下一个Token

    size_t get_pos() const {
        return pos;
    }
};

// 创建专门的词法错误类
class LexicalError : public std::runtime_error {
public:
    LexicalError(const std::string &message, size_t position)
        : std::runtime_error("Lexical error at position " +
                             std::to_string(position) + ": " + message),
          pos(position) {}

    size_t getPosition() const {
        return pos;
    }

private:
    size_t pos;
};

// 执行词法分析并输出结果到文件
void perform_lexical_analysis(
    const std::string &input_file, const std::string &output_file);

#endif