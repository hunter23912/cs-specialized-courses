#pragma once
#include <memory>
#include <string>
#include <vector>

#include "Lexer.h"

// AST节点
struct ASTNode {
    std::string type;
    std::string value;
    std::vector<std::shared_ptr<ASTNode>> children;

    std::string dataType;  // 数据类型（int, float, string等）

    ASTNode(const std::string& type, const std::string& value = "")
        : type(type), value(value), dataType("unknown") {}

    // 添加方法用于打印AST
    void print(int depth = 0) const {
        std::string indent(depth * 2, ' ');
        std::cout << indent << type;
        if (!value.empty()) {
            std::cout << ": " << value;
        }
        std::cout << std::endl;
        for (const auto& child : children) {
            child->print(depth + 1);
        }
    }
};

class Parser {
public:
    Parser(const std::vector<Token>& tokens);
    std::shared_ptr<ASTNode> parse();

private:
    const std::vector<Token>& tokens;
    size_t pos;
    Token current_token;

    void advance();
    void eat(const std::string& expected_type);

    std::shared_ptr<ASTNode> parseStatement();
    std::shared_ptr<ASTNode> parseExpression();
    std::shared_ptr<ASTNode> parseTerm();
    std::shared_ptr<ASTNode> parseFactor();
    std::shared_ptr<ASTNode> parseStatementSequence();
};