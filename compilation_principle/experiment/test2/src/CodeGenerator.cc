#include "CodeGenerator.h"

#include <fstream>
#include <iostream>

CodeGenerator::CodeGenerator() : tempCount(1) {}

std::string CodeGenerator::newTemp() {
    return "t" + std::to_string(tempCount++);
}

void CodeGenerator::generate(const std::shared_ptr<ASTNode>& ast) {
    if (ast) {
        generateNodeCode(ast);
    }
}

std::string CodeGenerator::generateNodeCode(
    const std::shared_ptr<ASTNode>& node) {
    if (!node) {
        return "";
    }

    // 处理基本类型
    if (node->type == "number") {
        return node->value;  // 数字直接返回其值
    } else if (node->type == "ident") {
        return node->value;  // 标识符直接返回其名称
    }
    // 处理一元运算符
    else if (node->type == "neg") {
        std::string operand = generateNodeCode(node->children[0]);
        std::string result = newTemp();
        quadruples.emplace_back("neg", operand, "", result);
        return result;
    }
    // 处理二元运算符
    else if (node->type == "plus" || node->type == "minus" ||
             node->type == "times" || node->type == "slash" ||
             node->type == "eql" || node->type == "neq" ||
             node->type == "lss" || node->type == "leq" ||
             node->type == "gtr" || node->type == "geq") {
        std::string left = generateNodeCode(node->children[0]);
        std::string right = generateNodeCode(node->children[1]);
        std::string result = newTemp();

        // 将语法树节点类型映射到四元式操作符
        std::string op;
        if (node->type == "plus")
            op = "+";
        else if (node->type == "minus")
            op = "-";
        else if (node->type == "times")
            op = "*";
        else if (node->type == "slash")
            op = "/";
        else if (node->type == "eql")
            op = "==";
        else if (node->type == "neq")
            op = "!=";
        else if (node->type == "lss")
            op = "<";
        else if (node->type == "leq")
            op = "<=";
        else if (node->type == "gtr")
            op = ">";
        else if (node->type == "geq")
            op = ">=";

        quadruples.emplace_back(op, left, right, result);
        return result;
    }
    // 处理赋值语句
    else if (node->type == "assign") {
        std::string ident = node->children[0]->value;            // 左值标识符
        std::string expr = generateNodeCode(node->children[1]);  // 表达式结果
        quadruples.emplace_back(":=", expr, "", ident);
        return ident;
    }
    // 处理条件语句和循环语句等其他类型
    else if (node->type == "program" || node->type == "seq") {
        std::string lastResult;
        for (const auto& child : node->children) {
            lastResult = generateNodeCode(child);
        }
        return lastResult;
    }

    return "";
}

const std::vector<Quadruple>& CodeGenerator::getQuadruples() const {
    return quadruples;
}

void CodeGenerator::saveToFile(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error(
            "Failed to open file for writing: " + filename);
    }

    for (const auto& quad : quadruples) {
        file << quad.toString() << std::endl;
    }
    file.close();
}

void CodeGenerator::clear() {
    quadruples.clear();
    tempCount = 1;
}

void generate_intermediate_code(
    const std::string& expr, const std::string& output_file) {
    try {
        // 词法分析
        Lexer lexer(expr);

        // 语法分析，生成AST
        Parser parser(lexer.tokens);
        auto ast = parser.parse();

        // 生成中间代码
        CodeGenerator generator;
        generator.generate(ast);

        // 保存到文件
        generator.saveToFile(output_file);

        std::cout << "Intermediate code generated and saved to " << output_file
                  << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error generating intermediate code: " << e.what()
                  << std::endl;
    }
}