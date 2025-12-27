#ifndef SEMANTIC_ANALYZER_H
#define SEMANTIC_ANALYZER_H

#include <memory>
#include <string>

#include "Parser.h"
#include "SymbolTable.h"

// 语义错误异常类
class SemanticError : public std::runtime_error {
public:
    SemanticError(const std::string& message)
        : std::runtime_error("Semantic error: " + message) {}
};

// 语义分析器类
class SemanticAnalyzer {
private:
    SymbolTable symbolTable;
    std::shared_ptr<ASTNode> ast;

    // 辅助方法
    void analyzeNode(const std::shared_ptr<ASTNode>& node);
    void analyzeProgram(const std::shared_ptr<ASTNode>& node);
    void analyzeConstDeclaration(const std::shared_ptr<ASTNode>& node);
    void analyzeVarDeclaration(const std::shared_ptr<ASTNode>& node);
    void analyzeProcDeclaration(const std::shared_ptr<ASTNode>& node);
    void analyzeStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeAssignStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeCallStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeIfStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeWhileStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeRepeatStatement(const std::shared_ptr<ASTNode>& node);
    void analyzeExpression(const std::shared_ptr<ASTNode>& node);

public:
    SemanticAnalyzer(const std::shared_ptr<ASTNode>& ast);

    // 执行语义分析
    void analyze();
};

#endif  // SEMANTIC_ANALYZER_H