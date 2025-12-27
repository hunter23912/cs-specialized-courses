#include "Parser.h"

#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

// Parser类的构造函数，初始化tokens、pos和current_token
Parser::Parser(const std::vector<Token>& tokens)
    : tokens(tokens),
      pos(0),
      current_token(tokens.empty() ? Token{"EOF", ""} : tokens[0]) {}

// 解析器的核心：递归下降分析
void Parser::advance() {
    if (pos + 1 < tokens.size()) {
        ++pos;
        current_token = tokens[pos];
    } else {
        current_token = {"EOF", ""};
    }
}

// 检查当前token是否为预期类型，如果是则前进，否则抛出异常
void Parser::eat(const std::string& expected_type) {
    if (current_token.type == expected_type) {
        advance();
    } else {
        throw std::runtime_error("Syntax error: expected " + expected_type +
                                 ", found " + current_token.type + " (" +
                                 current_token.value + ") at pos " +
                                 std::to_string(pos));
    }
}

// 入口：返回语法树根节点
std::shared_ptr<ASTNode> Parser::parse() {
    auto root = parseStatementSequence();
    if (current_token.type != "EOF") {
        throw std::runtime_error(
            "Syntax error: unexpected token after program end");
    }
    return root;
}

std::shared_ptr<ASTNode> Parser::parseStatementSequence() {
    auto seqNode = std::make_shared<ASTNode>("seq");
    // 只在不是EOF时解析语句
    while (current_token.type != "EOF" && current_token.type != "endsym" &&
           current_token.type != "untilsym") {
        seqNode->children.push_back(parseStatement());
        if (current_token.type == "semicolon") {
            eat("semicolon");
        } else {
            break;  // 如果不是分号，结束解析
        }
    }
    return seqNode->children.size() == 1 ? seqNode->children[0] : seqNode;
}

std::shared_ptr<ASTNode> Parser::parseStatement() {
    if (current_token.type == "ifsym") {
        auto ifNode = std::make_shared<ASTNode>("if");
        eat("ifsym");
        ifNode->children.push_back(parseExpression());
        eat("thensym");
        ifNode->children.push_back(parseStatement());
        if (current_token.type == "elsesym") {
            eat("elsesym");
            ifNode->children.push_back(parseStatement());
        }
        return ifNode;
    } else if (current_token.type == "beginsym") {
        eat("beginsym");
        auto blockNode = parseStatementSequence();
        eat("endsym");
        return blockNode;
    } else if (current_token.type == "repeatsym") {
        auto repeatNode = std::make_shared<ASTNode>("repeat");
        eat("repeatsym");
        repeatNode->children.push_back(parseStatementSequence());
        eat("untilsym");
        repeatNode->children.push_back(parseExpression());
        return repeatNode;
    } else if (current_token.type == "callsym") {
        auto callNode = std::make_shared<ASTNode>("call");
        eat("callsym");
        if (current_token.type != "ident") {
            throw std::runtime_error(
                "Syntax error: expected identifier after 'call' at pos " +
                std::to_string(pos));
        }
        callNode->children.push_back(
            std::make_shared<ASTNode>("ident", current_token.value));
        eat("ident");
        // 支持带参数的 call
        if (current_token.type == "lparen") {
            eat("lparen");
            auto argsNode = std::make_shared<ASTNode>("args");
            if (current_token.type != "rparen") {
                argsNode->children.push_back(parseExpression());
                while (current_token.type == "comma") {
                    eat("comma");
                    argsNode->children.push_back(parseExpression());
                }
            }
            eat("rparen");
            callNode->children.push_back(argsNode);
        }
        return callNode;
    } else if (current_token.type == "ident") {
        auto assignNode = std::make_shared<ASTNode>("assign");
        assignNode->children.push_back(
            std::make_shared<ASTNode>("ident", current_token.value));
        eat("ident");
        eat("becomes");
        assignNode->children.push_back(parseExpression());
        return assignNode;
    }
    throw std::runtime_error("Syntax error: unexpected token " +
                             current_token.type + " at pos " +
                             std::to_string(pos));
}

// 表达式递归下降分析树
std::shared_ptr<ASTNode> Parser::parseExpression() {
    auto left = parseTerm();
    while (current_token.type == "plus" || current_token.type == "minus" ||
           current_token.type == "eql" || current_token.type == "neq" ||
           current_token.type == "lss" || current_token.type == "gtr" ||
           current_token.type == "leq" || current_token.type == "geq") {
        std::string op = current_token.type;
        advance();
        auto opNode = std::make_shared<ASTNode>(op);
        opNode->children.push_back(left);
        opNode->children.push_back(parseTerm());
        left = opNode;
    }
    return left;
}

// 项递归下降分析树
std::shared_ptr<ASTNode> Parser::parseTerm() {
    auto left = parseFactor();
    while (current_token.type == "times" || current_token.type == "slash") {
        std::string op = current_token.type;
        advance();
        auto opNode = std::make_shared<ASTNode>(op);
        opNode->children.push_back(left);
        opNode->children.push_back(parseFactor());
        left = opNode;
    }
    return left;
}

// 因子递归下降分析树
std::shared_ptr<ASTNode> Parser::parseFactor() {
    if (current_token.type == "minus") {
        // 支持负数
        advance();
        auto negNode = std::make_shared<ASTNode>("neg");
        negNode->children.push_back(parseFactor());
        return negNode;
    }
    if (current_token.type == "ident") {
        auto node = std::make_shared<ASTNode>("ident", current_token.value);
        advance();
        return node;
    } else if (current_token.type == "number") {
        auto node = std::make_shared<ASTNode>("number", current_token.value);
        advance();
        return node;
    } else if (current_token.type == "lparen") {
        advance();
        auto node = parseExpression();
        eat("rparen");
        return node;
    }
    throw std::runtime_error(
        "Syntax error: expected identifier, number, or '(', but found '" +
        current_token.value + "' at pos " + std::to_string(pos));
}