#include <cctype>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

using namespace std;

// PL/0保留字集合
const set<string> reserved = {"const", "var", "procedure", "call", "begin", "end", "if", "then", "while", "do", "odd"};

// 函数声明
string readFile(const string &filename);                               // 读取文件内容
vector<string> extractIdentifiers(const string &code);                 // 提取标识符
map<string, int> countIdentifiers(const vector<string> &identifiers);  //  统计标识符出现次数
void printIdentifierCounts(const map<string, int> &identifier_counts); // 输出标识符统计结果

int main()
{

    string filename = "../input.txt";

    string code = readFile(filename); // 读取文件内容

    if (code.empty())
    {
        cerr << "Warning: file is empty." << endl;
        return 1;
    }

    // 提取标识符
    vector<string> identifiers = extractIdentifiers(code);

    // 统计标识符出现次数
    map<string, int> identifier_counts = countIdentifiers(identifiers);

    // 输出结果
    printIdentifierCounts(identifier_counts);

    return 0;
}

// 读取文件内容
string readFile(const string &filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cerr << "Error: Could not open file " << filename << endl;
        return "";
    }

    // 两个参数构造函数，第一个参数是一个istream对象，第二个参数是一个istream对象的结束迭代器
    string content((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();
    return content;
}

// 提取标识符
vector<string> extractIdentifiers(const string &code)
{
    vector<string> identifiers;
    string current_id;
    bool in_identifier = false;
    bool in_comment = false;

    // 遍历代码字符
    for (char c : code)
    {
        if (in_comment)
        {
            // 处理注释，直到遇到结束符号}
            if (c == '}')
            {
                in_comment = false;
            }
            continue;
        }
        else if (c == '{')
        {
            // 进入注释状态
            in_comment = true;
            continue;
        }

        // 处理标识符
        if (in_identifier)
        {
            if (isalnum(c)) // isalnum()函数判断字符是否是字母或数字
            {               // 字母或数字继续构成标识符
                current_id += tolower(c);
            }
            else
            {
                // 结束标识符识别
                in_identifier = false;

                // 非保留字则记录
                if (!current_id.empty() && reserved.find(current_id) == reserved.end())
                {
                    identifiers.push_back(current_id); // 非保留字则记录
                }
                current_id.clear();
            }
        }
        else
        {
            if (isalpha(c))
            { // 字母开始新的标识符
                in_identifier = true;
                current_id += tolower(c);
            }
        }
    }

    // 处理文件末尾可能未结束的标识符
    if (in_identifier && !in_comment)
    {
        if (!current_id.empty() && reserved.find(current_id) == reserved.end())
        {
            identifiers.push_back(current_id);
        }
    }

    return identifiers;
}

// 统计标识符出现次数
map<string, int> countIdentifiers(const vector<string> &identifiers)
{
    map<string, int> counts;
    for (const string &id : identifiers)
    {
        counts[id]++;
    }
    return counts;
}

// 输出标识符统计结果
void printIdentifierCounts(const map<string, int> &identifier_counts)
{
    cout << "Identifier counts:" << endl;
    for (const auto &pair : identifier_counts)
    {
        cout << pair.first << ": " << pair.second << endl;
    }
}