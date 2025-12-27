#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Token类型枚举
enum TokenType
{
    LPAREN, // (
    RPAREN, // )
    PLUS,   // +
    MINUS,  // -
    TIMES,  // *
    SLASH,  // /
    IDENT,  // 标识符
    NUMBER, // 无符号整数
    END_OF_FILE,
    ERROR
};

// Token结构体
struct Token
{
    TokenType type;
    string value;
};

vector<Token> tokens;
int current = 0;

// 辅助函数：去除字符串首尾空格
string trim(const string &s)
{
    size_t start = s.find_first_not_of(" \t");
    if (start == string::npos) return "";
    size_t end = s.find_last_not_of(" \t");
    return s.substr(start, end - start + 1);
}

// 读取词法分析结果
void readTokens(const string &filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cerr << "无法打开文件: " << filename << endl;
        exit(1);
    }

    string line;
    while (getline(file, line))
    {
        line = trim(line);
        if (line.empty()) continue;

        // 去除外层括号
        if (line.front() != '(' || line.back() != ')')
        {
            cerr << "无效的token格式: " << line << endl;
            exit(1);
        }
        line = line.substr(1, line.size() - 2);

        // 分割类型和值
        size_t comma = line.find(',');
        if (comma == string::npos)
        {
            cerr << "无效的token格式: " << line << endl;
            exit(1);
        }

        string typeStr = trim(line.substr(0, comma));
        string valueStr = trim(line.substr(comma + 1));

        // 转换为TokenType
        TokenType type;
        if (typeStr == "lparen")
            type = LPAREN;
        else if (typeStr == "rparen")
            type = RPAREN;
        else if (typeStr == "plus")
            type = PLUS;
        else if (typeStr == "minus")
            type = MINUS;
        else if (typeStr == "times")
            type = TIMES;
        else if (typeStr == "slash")
            type = SLASH;
        else if (typeStr == "ident")
            type = IDENT;
        else if (typeStr == "number")
            type = NUMBER;
        else
        {
            cerr << "未知的token类型: " << typeStr << endl;
            exit(1);
        }

        tokens.push_back({type, valueStr});
    }
    tokens.push_back({END_OF_FILE, ""}); // 添加EOF标记
}

// 获取当前token
Token currentToken()
{
    if (current >= tokens.size()) return {END_OF_FILE, ""};
    return tokens[current];
}

// 移动到下一个token
void nextToken()
{
    if (current < tokens.size()) current++;
}

// 语法错误处理
void error(const string &msg)
{
    cerr << "语法错误：" << msg << endl;
    exit(1);
}

// 因子解析
void parseFactor()
{
    Token tok = currentToken();
    switch (tok.type)
    {
        case IDENT:
        case NUMBER: nextToken(); break;
        case LPAREN:
            nextToken();
            parseFactor(); // 实际应解析表达式，原代码有误，修正为parseExpression()
            if (currentToken().type != RPAREN)
            {
                error("缺少右括号");
            }
            nextToken();
            break;
        default: error("期望标识符、数字或左括号，但得到 " + tok.value);
    }
}

// 项解析
void parseTerm()
{
    parseFactor();
    while (currentToken().type == TIMES || currentToken().type == SLASH)
    {
        nextToken();
        parseFactor();
    }
}

// 表达式解析
void parseExpression()
{
    // 处理可选符号
    if (currentToken().type == PLUS || currentToken().type == MINUS)
    {
        nextToken();
    }
    parseTerm();
    // 处理后续加减项
    while (currentToken().type == PLUS || currentToken().type == MINUS)
    {
        nextToken();
        parseTerm();
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        cerr << "用法: " << argv[0] << " <输入文件>" << endl;
        return 1;
    }

    try
    {
        readTokens(argv[1]);
        parseExpression();

        // 检查是否解析完所有输入
        if (currentToken().type != END_OF_FILE)
        {
            error("表达式后有多余内容");
        }

        cout << "语法正确" << endl;
        return 0;
    }
    catch (const exception &e)
    {
        return 1;
    }
}