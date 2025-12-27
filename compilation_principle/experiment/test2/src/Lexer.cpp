#include "Lexer.h"

// 构造函数：初始化文本、位置、当前字符，并定义关键字映射
Lexer::Lexer(const std::string &text)
    : text(text), pos(0), current_char(text.empty() ? '\0' : text[0]) {
    // 增加 for、repeat、until 等关键字
    keywords = {{"const", "constsym"},
        {"var", "varsym"},
        {"procedure", "procsym"},
        {"call", "callsym"},
        {"begin", "beginsym"},
        {"end", "endsym"},
        {"if", "ifsym"},
        {"then", "thensym"},
        {"else", "elsesym"},
        {"while", "whilesym"},
        {"do", "dosym"},
        {"read", "readsym"},
        {"write", "writesym"},
        {"odd", "oddsym"},
        {"for", "forsym"},
        {"to", "tosym"},
        {"repeat", "repeatsym"},
        {"until", "untilsym"}};
}

// 移动到下一个字符
void Lexer::advance() {
    pos++;
    if (pos < text.length()) {
        current_char = text[pos];
    } else {
        current_char = '\0';
    }
}

// 跳过空白字符
void Lexer::skip_whitespace() {
    while (current_char != '\0' && std::isspace(current_char)) {
        advance();
    }
}

void Lexer::skip_comment() {
    if (current_char == '/' && peek_next() == '*') {
        advance();
        advance();  // 跳过“/*”
        while (!(current_char == '*' && peek_next() == '/')) {
            if (current_char == '\0')
                throw LexicalError("Unmatched comment", pos);
            advance();
        }
        advance();
        advance();  // 跳过“*/”
    }
}

// 识别标识符或关键字
Token Lexer::_id() {
    std::string result;
    while (std::isalnum(current_char)) {
        result += std::tolower(current_char);
        advance();
    }
    auto it = keywords.find(result);
    return it != keywords.end() ? Token{it->second, result}
                                : Token{"ident", result};
}

// 识别数字常量
Token Lexer::_number() {
    std::string num_str;
    bool has_decimal = false;  // 是否有小数点

    // 第一部分：收集数字和最多一个小数点
    while (std::isdigit(current_char) || current_char == '.') {
        if (current_char == '.') {
            if (has_decimal) {
                // 遇到第二个小数点时，抛出错误
                throw LexicalError(
                    "Invalid number format: Multiple decimal points in number "
                    "'" +
                        num_str + ".'",
                    pos);
            }
            has_decimal = true;
        }
        num_str += current_char;
        advance();
    }

    // 处理特殊情况：数字后紧跟着字母
    if (std::isalpha(current_char)) {
        std::string invalid = num_str + current_char;
        size_t error_pos = pos;  // 记录当前错误位置
        while (std::isalnum(current_char)) {
            invalid += current_char;
            advance();
        }
        throw LexicalError(
            "Invalid number format: '" + invalid + "'", error_pos);
    }

    return {"number", num_str};
}

Token Lexer::_string() {
    std::string str_value;
    advance();
    while (current_char != '\0' && current_char != '\'') {
        str_value += current_char;
        advance();
    }
    if (current_char == '\'') {
        advance();
        return {"string", str_value};
    } else {
        size_t error_pos = pos;
        throw LexicalError(
            "Unclosed string at position " + std::to_string(error_pos),
            error_pos);
    }
}

// 获取下一个字符
char Lexer::peek_next() const {
    return (pos + 1 < text.size()) ? text[pos + 1] : '\0';
}

// 处理运算符 “:=”
Token Lexer::process_colon() {
    advance();  // 跳过“:”
    if (current_char == '=') {
        advance();  // 跳过“=”
        return {"becomes", ":="};
    }
    throw LexicalError("Expected '=' after ':', but found '" +
                           std::string(1, current_char) + "'",
        pos);
}

// 处理”<”和”<=”和”<>”
Token Lexer::process_less() {
    advance();
    if (peek_next() == '=') {
        advance();
        return {"leq", "<="};
    }
    if (peek_next() == '>') {
        advance();
        return {"neq", "<>"};
    }
    return {"lss", "<"};
}

// 处理”>”和”>=”
Token Lexer::process_greater() {
    advance();
    if (peek_next() == '=') {
        advance();
        return {"geq", ">="};
    }
    return {"gtr", ">"};
}

// 处理单字符运算符和分隔符
Token Lexer::process_single_char() {
    switch (current_char) {
        case '+':
            advance();
            if (current_char == '+')  // 检查是否是连续的 "+"
            {
                throw LexicalError("Unexpected operator '++' at position " +
                                       std::to_string(pos - 1),
                    pos - 1);
            }
            return {"plus", "+"};
        case '-':
            advance();
            if (current_char == '-')  // 检查是否是连续的 "-"
            {
                throw LexicalError("Unexpected operator '--' at position " +
                                       std::to_string(pos - 1),
                    pos - 1);
            }
            return {"minus", "-"};
        case '|':
            advance();
            if (current_char == '|')  // 检查是否是连续的 "|"
            {
                throw LexicalError("Unexpected operator '||' at position " +
                                       std::to_string(pos - 1),
                    pos - 1);
            }
            throw LexicalError("Unexpected character '|' at position " +
                                   std::to_string(pos - 1),
                pos - 1);
        case '*': advance(); return {"times", "*"};
        case '/': advance(); return {"slash", "/"};
        case '(': advance(); return {"lparen", "("};
        case ')': advance(); return {"rparen", ")"};
        case '=': advance(); return {"eql", "="};
        case ',': advance(); return {"comma", ","};
        case '.': advance(); return {"period", "."};
        case ';': advance(); return {"semicolon", ";"};
        default:
            // 更详细的错误信息
            std::string message = "Unexpected character '";
            message += current_char;
            message += "'";
            throw LexicalError(message, pos);
    }
}

// 获取下一个词法单元
Token Lexer::get_next_token() {
    try {
        // 遍历文本，直到文件末尾
        while (current_char != '\0') {
            if (std::isspace(current_char))  // 跳过空白字符
            {
                skip_whitespace();
                continue;
            }
            if (current_char == '/' && peek_next() == '*')  // 跳过注释
            {
                skip_comment();
                continue;
            }
            if (std::isalpha(current_char))  // 如果是字母，识别标识符或关键字
            {
                return _id();
            }

            if (std::isdigit(current_char))  // 如果是数字，识别数字常量
            {
                return _number();
            }
            if (current_char == '\'')  // 如果是单引号，识别字符串常量
            {
                return _string();
            }
            if (current_char == ':')  // 处理多字符运算符 ":="
            {
                return process_colon();
            }
            if (current_char == '<')  // 处理"<"和"<="和"<>"
            {
                return process_less();
            }
            if (current_char == '>')  // 处理">"和">="
            {
                return process_greater();
            }

            // 处理单字符运算符和分隔符
            return process_single_char();
        }

        // 到达文件末尾
        return {"EOF", ""};
    } catch (const LexicalError &e) {
        std::cerr << e.what() << std::endl;

        // 错误恢复：跳过当前字符，返回错误标记
        // 但不终止词法分析
        advance();
        return {"ERROR", "error"};
    }
}

void Lexer::setTokens(const std::vector<Token> &tokens) {
    this->tokens = tokens;  // 设置词法单元
    this->current_token_index = 0;
    if (!tokens.empty()) {
        current_token = tokens[0];  // 初始化当前Token
    } else {
        current_token = {"EOF", ""};  // 如果没有Token，设置为EOF
    }
}

Token Lexer::get_current_token() const {
    return current_token;  // 返回当前Token
}

void Lexer::advance_token() {
    if (current_token_index + 1 < tokens.size()) {
        current_token_index++;                        // 移动到下一个Token
        current_token = tokens[current_token_index];  // 更新当前Token
    } else {
        current_token = {"EOF", ""};  // 如果没有更多Token，设置为EOF
    }
}

// 执行词法分析并输出结果到文件
void perform_lexical_analysis(
    const std::string &input_file, const std::string &output_file) {
    std::ifstream input(input_file);  // 打开输入文件
    if (!input.is_open()) {
        throw std::runtime_error(
            " (from perform_lexical_analysis())Input file not found: " +
            input_file);
    }

    // 读取文件内容到字符串text
    std::string text((std::istreambuf_iterator<char>(input)),
        std::istreambuf_iterator<char>());
    input.close();

    Lexer lexer(text);          // 创建词法分析器
    std::vector<Token> tokens;  // 存储所有词法单元

    // 逐个获取词法单元，直到文件结束
    while (true) {
        Token token = lexer.get_next_token();
        if (token.type == "EOF") break;
        tokens.push_back(token);
    }

    // 将词法分析结果写入输出文件
    std::ofstream output(output_file);
    for (const auto &token : tokens) {
        output << "(" << token.type << ", " << token.value << ")\n";
    }
    output.close();
}
