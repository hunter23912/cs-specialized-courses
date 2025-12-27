#ifndef CODE_GENERATOR_H
#define CODE_GENERATOR_H

#include <memory>
#include <string>
#include <vector>

#include "Parser.h"

// 四元式结构
struct Quadruple {
    std::string op;      // 运算符
    std::string arg1;    // 第一个操作数
    std::string arg2;    // 第二个操作数
    std::string result;  // 结果

    Quadruple(const std::string& op, const std::string& arg1,
        const std::string& arg2, const std::string& result)
        : op(op), arg1(arg1), arg2(arg2), result(result) {}

    // 转换为字符串表示
    std::string toString() const {
        return "( " + op + ", " + arg1 + ", " + arg2 + ", " + result + " )";
    }
};

// 代码生成器类
class CodeGenerator {
private:
    std::vector<Quadruple> quadruples;  // 四元式序列
    int tempCount;                      // 临时变量计数器

    // 生成新的临时变量名
    std::string newTemp();

    // 递归生成AST节点的中间代码
    std::string generateNodeCode(const std::shared_ptr<ASTNode>& node);

public:
    CodeGenerator();

    // 从AST生成中间代码
    void generate(const std::shared_ptr<ASTNode>& ast);

    // 获取生成的四元式序列
    const std::vector<Quadruple>& getQuadruples() const;

    // 将四元式序列保存到文件
    void saveToFile(const std::string& filename) const;

    // 清空四元式序列
    void clear();
};

// 从表达式字符串生成四元式并保存到文件
void generate_intermediate_code(
    const std::string& expr, const std::string& output_file);

#endif  // CODE_GENERATOR_H